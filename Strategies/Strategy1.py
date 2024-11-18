import backtrader as bt

class TestStrategy(bt.Strategy):
    params = (
        ('rsi_period', 30),  
        ('rsi_oversold', 30),  # sobreventa
        ('rsi_overbought', 70),  # sobrecompra
        ('printlog', True),
        ##Vela - Hombre colgado 
        ('periodo_alcista', 3),
        ('cuerpo_tamanio_max', 0.40),   # % del rango del dia
        ('mecha_inferior_tamanio_min', 1),   
        ('mecha_superior_tamanio_max', 0.3),
        ##SMA
        ('sma_period', 40),  # Período del SMA
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        if self.params.printlog:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Indicador RSI
        self.rsi = bt.indicators.RelativeStrengthIndex(
            self.datas[0], period=self.params.rsi_period)
        
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        # Guardar el balance inicial
        self.starting_cash = self.broker.getvalue()

        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.sma_period)

    def es_hombreColgado(self, i):
        rango_total = self.datahigh[i] - self.datalow[i]
        cuerpo = abs(self.dataclose[i] - self.dataopen[i])

        if cuerpo > rango_total * self.params.cuerpo_tamanio_max:
            return False

        if self.dataclose[i] > self.dataopen[i]:
            mecha_inferior = self.dataopen[i] - self.datalow[i]
        else:
            mecha_inferior = self.dataclose[i] - self.datalow[i]

        # Verifica si la mecha inferior es suficientemente grande
        if mecha_inferior < cuerpo * self.params.mecha_inferior_tamanio_min:
            return False

        if self.dataclose[i] > self.dataopen[i]:
            mecha_superior = self.datahigh[i] - self.dataclose[i]
        else:
            mecha_superior = self.datahigh[i] - self.dataopen[i]

        if mecha_superior >= cuerpo * self.params.mecha_superior_tamanio_max:
            return False

        return True


    def next(self):
        # Registra el precio de cierre
        self.log('Close, %.2f' % self.dataclose[0])

        if self.rsi[0] < self.params.rsi_oversold and self.rsi[-1] >= self.params.rsi_oversold:# hacia arriba
            self.log(f'BUY CREATE, Precio: {self.dataclose[0]}')
            self.order = self.buy()
            return

        elif self.rsi[0] > self.params.rsi_overbought and self.rsi[-1] <= self.params.rsi_overbought:#hacia abajo
            self.log(f'SELL CREATE, Precio: {self.dataclose[0]}')
            self.order = self.sell()
            return

        if len(self.data) >= self.params.periodo_alcista and all(self.dataclose[-i] > self.dataclose[-i-1] for i in range(1, self.params.periodo_alcista)):
            if self.es_hombreColgado(0):
                self.log(f'Vela - Hombre colgado Detectado: Precio {self.dataclose[0]}')
                if self.position:
                    self.log(f'SELL CREATE, Precio: {self.dataclose[0]}')
                    self.sell()
                    return

        # Condición de compra cuando el precio está por encima del SMA
        if self.datas[0].close[0] > self.sma[0]:  
            self.log(f'BUY CREATE, Precio: {self.datas[0].close[0]:.2f}')
            self.buy()

        # Condición de venta cuando el precio está por debajo del SMA
        elif self.datas[0].close[0] < self.sma[0] and self.position : 
            self.log(f'SELL CREATE, Precio: {self.datas[0].close[0]:.2f}')
            self.sell()

    def stop(self):
        # Calcular balance final
        self.final_value = self.broker.getvalue()
        self.log(f'Balance inicial: {self.starting_cash:.2f}')
        self.log(f'Balance final: {self.final_value:.2f}')
        self.log(f'Ganancia/Pérdida: {self.final_value - self.starting_cash:.2f}')
