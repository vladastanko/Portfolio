#BACKTEST PARAMETERS
candle                                  = 'hourly'
start_date                              = "2021-01-01 09:15:00"
end_date                                = "2023-01-01 09:15:00"
total_capital                           = 1000000

##POSITIONS
position_size                           = 100000
target_in_percentage                    = 2.5
stoploss_in_percentage                  = 10
trailing_stoploss                       = False
Exit_if_criteria_met_even_if_loss       = False

##SHORT AND LONG EMA/HMA
short_hma_length                        = 20
long_hma_length                         = 50
short_ema_length                        = 20
long_ema_length                         = 50

##SHORT AND LONG EMA/HMA TRENDS
short_hma_trend_duration                = 3
short_ema_trend_duration                = 3
long_hma_trend_duration                 = 3
long_ema_trend_duration                 = 3

##SHORT AND LONG HMA AND EMA RELATIONSHIPS
short_hma_long_hma_trend_duration       = 3
short_hma_long_ema_trend_duration       = 3
short_ema_long_ema_trend_duration       = 3
long_hma_long_ema_trend_duration        = 3
long_hma_short_ema_trend_duration       = 3
short_hma_short_ema_trend_duration      = 3

##STOCHASTIC PARAMETERS:
stoch_k                                 = 4
stoch_d                                 = 3
smooth_k                                = 3

##STOCHASTIC MOMENTUM PARAMETERS:
K_Length                                = 3
K_Smoothing_Length                      = 3
K_Double_Smoothing_Length               = 3
Signal_Length                           = 3

##NADARAYA-WATSON PARAMETERS:
h                                       = 8
r                                       = 8
x_0                                     = 25
smooth_colors                           = False
lag                                     = 2
