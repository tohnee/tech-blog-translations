---
title: "DeepMind, meet Android"
source: https://deepmind.google/blog/deepmind-meet-android/
site: deepmind
date: 2018-05-08
authors: 
crawled: 2026-09-13
---

We’re delighted to announce a new collaboration between [DeepMind for Google](https://deepmind.com/about/deepmind-for-google) and Android, the world’s most popular mobile operating system. Together, we’ve created two new features that will be available to people with devices running Android P later this year:

- Adaptive Battery: A smart battery management system that uses machine learning to anticipate which apps you’ll need next, providing a more reliable battery experience.
- Adaptive Brightness: A personalised experience for screen brightness, built on algorithms that learn your brightness preferences in different surroundings.

This is an exciting first for us. Our previous work with Google has been built on massive-scale infrastructure, including projects to [reduce energy use](https://deepmind.com/blog/article/deepmind-ai-reduces-google-data-centre-cooling-bill-40) in data centres, optimise recommendations in Google Play, and bring WaveNet voices to the [Google Assistant](https://deepmind.com/blog/article/wavenet-launches-google-assistant) and to [Google Cloud Platform](https://cloud.google.com/text-to-speech/docs/wavenet) customers across the world.

But this time we’re deploying techniques that run on the compute power of a single mobile device—that’s orders of magnitude less than typical machine learning applications. Here’s how they work:

## Adaptive Battery

Android has worked to improve battery life with each release of its operating system. That shouldn’t be surprising, since [surveys](https://today.yougov.com/topics/technology/articles-reports/2018/02/20/smartphone-users-still-want-longer-battery-life) of smartphone users show that battery life is a top priority.

Today, battery power is spent keeping apps up-to-date in the [background](https://developer.android.com/about/versions/oreo/background) so that they’re fresh when users open them next. But nobody uses all the apps on their phone with the same frequency, so in many cases that battery use might not be necessary.

To help tackle this, we’ve partnered with the Android team to develop a feature called Adaptive Battery that uses a deep [convolutional neural net](https://en.wikipedia.org/wiki/Convolutional_neural_network) to predict which apps you’ll use in the next few hours and which you probably won’t use until later.

Using that knowledge, Android adapts to your usage patterns so that it only spends battery power on the apps you’ll need. The initial results have been very promising, and we’ve seen a significant reduction in background activity in our internal testing.

## Adaptive Brightness

Sometimes your screen can be frustratingly dim on a bright, sunny day or too bright when you reach over to check your phone in the middle of the night. That’s because the system is one size fits all, and doesn't account for your personal preferences. So you need to make adjustments manually—for example, turning screen brightness down to read in bed at night and back up when you wake up in the morning.

To improve this experience, we've partnered with Android to incorporate machine learning into a feature called Adaptive Brightness. The feature now learns how you set the brightness slider for the ambient light of your surroundings, and then adjusts the screen brightness according to your preferences. During our internal testing, a considerable proportion of Android P users made fewer manual brightness adjustments.

We’re excited to be working with the amazing Android team to try to save energy while making people’s lives easier, and look forward to more to come. And if you’re interested in working on real-world machine learning challenges, from global-scale infrastructure to on-device optimisation, then the DeepMind for Google team is [always looking for exceptional people](https://deepmind.com/careers/)!
