# Intensity_from_focal_scan
calc I for focal diameter for a focal scan


reads csv 
for given columns can the intensity calculated if additional parameters as pulse duration in [s] and laser energy [J] are provided. Here the scaling of focal diameter from the columns is [um], a third column gives the q-factor which gives the 
energy content in the focal area. 

Theoretical calculation for either IL (intensity) or IL_peak are added, calculation of dimensionless vector potential a0 and a0_peak
added. Plots together with the experimental result. 
One can align the theoretical values by a mulitlication with a scale factor. 
A longer laser pulse by the introduction of the Group delay dispersion parameter (GDD) is added. 
The peak calculation assumes, that the evaluation (or theoretical calculation) was done in 1/e - by this peak is calculated with just multiplying with a factor of 2.7. For example in PIC simulations the a0 parameter is usually given in peak...

