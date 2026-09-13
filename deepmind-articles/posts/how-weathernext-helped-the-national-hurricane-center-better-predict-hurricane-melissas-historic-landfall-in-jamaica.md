---
title: "How WeatherNext helped the National Hurricane Center better predict Hurricane Melissa’s historic landfall in Jamaica"
source: https://deepmind.google/blog/how-weathernext-helped-the-national-hurricane-center-better-predict-hurricane-melissas-historic-landfall-in-jamaica/
site: deepmind
date: 2026-05-19
authors: WeatherNext team
crawled: 2026-09-13
---

The National Hurricane Center was able to issue advanced weather warnings to give communities in Jamaica additional lead time to prepare, evacuate, and help protect livelihoods

In October 2025, Hurricane Melissa made history. It was the strongest hurricane on record to land in Jamaica and tied for the strongest hurricane in the Atlantic.

The National Hurricane Center’s (NHC) forecast also marked a historic milestone. For the first time, they predicted a storm would reach Category 5 intensity starting from Category 1 wind speed. Our AI model [WeatherNext](https://deepmind.google/science/weathernext/) helped the NHC make this decision by predicting the storm’s rapid intensification and landfall in Jamaica with high confidence—and most critically, this prediction came five days in advance.

Predicting dangerous storms earlier and more accurately helps teams on the ground to better mobilize resources and coordinate evacuations effectively.

[ Your browser does not support the video tag.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/9LLVffEBUW8TWF_I/weathernext__case-study__bg.webm)

Watch how WeatherNext provided accurate, early forecasting for 2025’s Hurricane Melissa and its Category 5 landfall in Jamaica.

## The challenge of rapid intensification

Predicting a storm’s path is difficult, but predicting a sudden jump in strength - known as “rapid intensification” - is even harder. This occurs when a hurricane's winds increase by at least 35 mph in just 24 hours. These events are very difficult to predict and also exceedingly dangerous because a weak system can transform into a major hurricane overnight, leaving little time to prepare.

> Tropical storms and hurricanes can change very quickly in terms of their structure and their intensity, which makes them more challenging to predict than other types of weather systems.

Michael Brennan

Director, National Hurricane Center

Historically, meteorologists faced a trade-off: larger global models were excellent at predicting a storm’s path, but often lacked the resolution to see the small-scale thunderstorms that drove its “engine”. Conversely, high-resolution local models could better see intensity, but lacked global context for accurate track forecasting. This meant that models either excelled at predicting a tropical cyclone's track, or its intensity, but not both.

## A scientific breakthrough with WeatherNext

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

An ensemble of predicted tracks for Hurricane Melissa from seven days before landfall down to October 28th 2025, when Hurricane Melissa made landfall in Jamaica as a Category 5 storm.

Developed by Google DeepMind and Google Research, our AI weather model WeatherNext bridges this historical gap by excelling at predicting both track and intensity. As part of Google's [Earth AI](https://ai.google/earth-ai/) initiative, the model achieves this dual capability by training on decades of global weather patterns alongside specialized datasets of extreme tropical cyclones.

Rather than providing a single “best guess,” WeatherNext can run ensembles of 50 different "what-if" scenarios, giving experts a broader range of possibilities to inform decision-making. We made this data available to everyone as an experimental showcase through [Weather Lab](https://deepmind.google.com/science/weatherlab?utm_source=&utm_medium=&utm_campaign=&utm_content=&_gl=1*147gps6*_ga*MTIxNTc3OTU3MC4xNzc2MTY5NzM4*_ga_LS8HVHCNQ0*czE3NzYxNjk3MzgkbzEkZzEkdDE3NzYxNjk4MjQkajU3JGwwJGgw).

When Hurricane Melissa was first identified as a weak tropical depression, traditional models wavered on whether it would strike Haiti as a weak system or intensify toward Jamaica. WeatherNext, however, predicted a Category 5 strength landfall in Jamaica five days in advance with 80% confidence, which increased to near 100% three days in advance. This was the first time a storm was successfully predicted to reach Category 5 strength starting from such a low initial wind speed. Identifying a top-tier hurricane from such modest beginnings marks a historic turning point in the ability to anticipate extreme intensification events.

Striking late in the Atlantic hurricane season, Melissa arrived after NHC forecasters had already spent months validating and gaining confidence in WeatherNext. On average, WeatherNext consistently performed exceptionally well for both track and intensity. This performance gave forecasters confidence in situations like Melissa, where both intensity and landfall prediction were critical.

![WeatherNext achieves state-of-the-art performance in predicting tropical cyclone tracks and intensities. Chart shows 2025 weighted average data for merged Atlantic and North Pacific regions.](https://lh3.googleusercontent.com/fBWnJ6TUGlMVaR27KiPpDJouf9hm9WXsvcNnDG-ZqoCUTGOQtvUeWPET_JG0v1lNES5D7uDtJ37mKEKHoXhwpQps0-IIXzOQ1mNpAtB_hSzJTfKqRAw=w1440)![WeatherNext achieves state-of-the-art performance in predicting tropical cyclone tracks and intensities. Chart shows 2025 weighted average data for merged Atlantic and North Pacific regions.](https://lh3.googleusercontent.com/Iy_incPkUbjZSNlR5gyVUMhKzN3kJLNgnXiQoQTSVfn3hp414r4IaP96dyViiWf6ZZijVwlsY3hoLoQcUv1wX2luxDrnHkJXRHnEOkps9sKRDqhm1g=w1440)

WeatherNext achieves exceptional performance in predicting tropical cyclone tracks and intensities. Chart shows 2025 individual operational models weighted average data for merged Atlantic and North Pacific regions. Plot compiled based on data in the [NHC’s annual verification report](https://www.nhc.noaa.gov/verification/pdfs/Verification_2025.pdf).

## Helping protect communities on the ground

![Evan Thompson, Principal Director of the Meteorological Service Jamaica, looking out over the city of Kingston under an overcast sky from a rooftop balcony.](https://lh3.googleusercontent.com/KTo4xuv5qXlJDL7NEAWoOL0G81yB3YYpNfzuru9uWpDrxNP81agTvxtIn2-CXsKIqFmUaFK2NqYqmKdEAR5BqHYUTBB0d06yUzumijBZmOaPDVP2=w1440-h810-n-nu)

Evan Thompson is the Principal Director, Meteorological Service Jamaica based in Kingston, Jamaica.

The NHC serves as the World Meteorological Organization's (WMO) Regional Specialized Meteorological Center for tropical cyclones for the Atlantic and Eastern Pacific, providing forecasts and warnings for nearly 30 countries.

Supported by WeatherNext’s predictions, along with physics-based models like HAFS, and real-time data from satellites and hurricane hunters, the NHC was able to provide the Meteorological Service Jamaica with unprecedented lead time. This allowed local officials to mobilize resources and coordinate evacuations effectively.

> With early evacuation and better preparation, that reduction in harm really does make a difference to our people. [...] It does actually save their lives, and it saves the livelihoods that they want to secure.

Evan Thompson

Principal Director, Meteorological Service Jamaica

## Scaling global safety

The impact of WeatherNext’s use during Hurricane Melissa is the result of a multi-year collaboration between Google and the NHC. Across the 2025 hurricane season the [NHC’s annual verification report](https://www.nhc.noaa.gov/verification/pdfs/Verification_2025.pdf) found that WeatherNext was the top-performing individual model for track and intensity supporting expert decision-making. As the upcoming hurricane season begins, we will continue to work alongside the NHC. We will remain an integral part of the NHC track and intensity guidance suite and hope our models can be useful in supporting their critical life-saving work.

We are also actively bringing these research capabilities to other critically affected regions, including the Philippines (PAGASA), Taiwan (CWA), Indonesia (BMKG) and Vietnam (VNMHA). Future priorities will also include collaborations with local agencies in Japan, Australia, and India where we want to continue this research in partnership with local experts. In all of these research efforts, all official weather alerts and warnings are issued solely by the respective national meteorological authorities.

By combining the speed and accuracy of AI with the irreplaceable experience of expert forecasters, we aim to reduce the [human and economic](https://www.nber.org/digest/202409/value-improving-hurricane-forecasts) toll of natural disasters.

We’ve already integrated this technology into forecasts on Search in geographic areas covered by NOAA and are working to expand access to other regions.

**Note: For official weather forecasts and warnings, refer to your local meteorological agency or national weather service.**

[Visit Weather Lab](https://deepmind.google.com/science/weatherlab?utm_source=&utm_medium=&utm_campaign=&utm_content=&_gl=1*147gps6*_ga*MTIxNTc3OTU3MC4xNzc2MTY5NzM4*_ga_LS8HVHCNQ0*czE3NzYxNjk3MzgkbzEkZzEkdDE3NzYxNjk4MjQkajU3JGwwJGgw)[Read the NHC’s report on Hurricane Melissa](https://www.nhc.noaa.gov/data/tcr/AL132025_Melissa.pdf)[Read the NHC’s report on the 2025 hurricane season](https://www.nhc.noaa.gov/verification/pdfs/Verification_2025.pdf)

## Acknowledgements

We thank Ferran Alet, Tom Andersson, Ilan Price, Stratis Markou, Andrew El-Kadi , Dominic Masters, Amy Li, Samier Merchant, Natalie Williams, Gregory Thornton, Ken MacKay, Olivia Graham, Ben Gaiarin, Elinor Kruse, Akib Uddin, Juanita Bawagan, Armin Senoner, Devaja Shah, Jacklynn Stott, Remi Lam, Aaron Bell, Paul Komarek, Matthew Willson, Alvaro Sanchez-Gonzalez and Peter Battaglia.

We also thank the teams at the National Hurricane Center, UK Met Office and the Cooperative Institute for Research in the Atmosphere.

Finally, we thank Raia Hadsell, Zoubin Ghahramani, Yossi Matias, Demis Hassabis for their support of this work.
