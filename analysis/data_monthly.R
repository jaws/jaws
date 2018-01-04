data_monthly <- aist_gcnet_edited.df[1:721, ,drop=F]
data_monthly <- transform(data_monthly, date= as.Date(JulianDecimalTime, origin=as.Date("2012-12-31")))
# Remove a column:  data2013 <- subset(data2013, select = -c(year))

write.csv(data_monthly, file = 'data_monthly.csv')

library(ggplot2)
theme_set(theme_gray())

# Allow Default X Axis Labels
ggplot(data_monthly, aes(x=date, y= TC_AirTemperature1)) +
  geom_point(aes(colour = TC_AirTemperature1)) +
  scale_colour_gradient2(low = "blue", mid = "green" , high = "red", midpoint = 0) + 
  geom_smooth(colour = "red",size = 1) +
  #geom_line(aes(y=TC_AirTemperature1)) +
  scale_y_continuous(limits = c(-50,-15), breaks = seq(-50,-15,5)) +
  labs(title="Monthly Plot", 
       subtitle="Change in TC_AirTemperature1", 
       caption="Source: GCNet", 
       x = "Date",
       y="Temperature (in degC)")



ggplot(data_monthly, aes(x=date, y= MaxAirTemperature1)) +
  geom_point(aes(colour = MaxAirTemperature1)) +
  scale_colour_gradient2(low = "blue", mid = "green" , high = "red", midpoint = 0) + 
  geom_smooth(colour = "red",size = 1) +
  #geom_line(aes(y=TC_AirTemperature1)) +
  scale_y_continuous(limits = c(-50,-15), breaks = seq(-50,-15,5)) +
  labs(title="Monthly Plot", 
       subtitle="Change in MaxAirTemperature1", 
       caption="Source: GCNet", 
       x = "Date",
       y="Temperature (in degC)")
