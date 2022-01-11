# CHALLENGE 142
## Seam Carving
###### Project 5: 11/1/2022

I have currently only implemented a horizontal shrinking version of seam carving although I plan to allow both stretching and shrinking horizontally and vertically when I return to this project but in C++.
Additionally, I might also return to this project if I decide to learn multiprocessing in python at some point because currently it is quite slow and I cannot think of any obvious optimisations other than multiprocessing. My only idea is to remove the pop() functions as I know they take quite a bit of performance however I am unsure of the best way to remove them while not gaining excess speed in my solutions.

Regardless, I think this algorithm is extremely interesting although I don't see it having much practical use beyond very few and specific images.

## Example input and output
Image source: https://en.wikipedia.org/wiki/Seam_carving
Scalled from 274x186 to 170x186
![Reference image](/ChallengesFolder/142-SeamCarving/Python/ReferenceImage.png) ![Output image](/ChallengesFolder/142-SeamCarving/Python/OutputImage.png)

## Examples of the backend process
![Gradient stage](/ChallengesFolder/142-SeamCarving/Python/Output/A-2.png)
![Seam stage](/ChallengesFolder/142-SeamCarving/Python/Output/B-2.png)
