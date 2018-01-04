aist_gcnet_edited.df <- data.frame(aist_gcnet_edited)
data_daily <- aist_gcnet_edited.df[1:25, ,drop=F]
data_daily <- transform(data_daily, date= as.Date(JulianDecimalTime, origin=as.Date("2012-12-31")))
# Remove a column:  data2013 <- subset(data2013, select = -c(year))

library(ggplot2)
theme_set(theme_gray())

# Allow Default X Axis Labels
ggplot(data_daily, aes(x=date, y= TC_AirTemperature1)) + 
  geom_point(aes(colour = TC_AirTemperature1)) +
  scale_colour_gradient2(low = "blue", mid = "green" , high = "red", midpoint = -45) + 
  geom_point(colour = "blue") +
  geom_smooth(colour = "red",size = 1) +
  #geom_line(aes(y=TC_AirTemperature1)) + 
  scale_y_continuous(limits = c(-50,-40), breaks = seq(-50,-40,2)) +
  labs(title="Daily Plot",
       subtitle="Change in TC_AirTemperature1", 
       caption="Source: GCNet", 
       x = "Date",
       y="Temperature (in degC)")


