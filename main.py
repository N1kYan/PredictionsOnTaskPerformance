# Main Python File
from DiscreteDistributionReader import DiscreteDistributionReader

# dr = DiscreteDistributionReader(path="curve.png", points=5)
dr1 = DiscreteDistributionReader(path="pdf_1.jpg", points=5)
dr2 = DiscreteDistributionReader(path="pdf_2.jpg", points=5)
dr3 = DiscreteDistributionReader(path="pdf_3.jpg", points=5)

dr1.plot()
dr2.plot()
dr3.plot()

scores1 = [round(dr1.brier_score(i), 2) for i in range(0, 6)]
scores2 = [round(dr2.brier_score(i), 2) for i in range(0, 6)]
scores3 = [round(dr3.brier_score(i), 2) for i in range(0, 6)]

print("Brier Scores for Task 1 are: ", scores1)
print("Brier Scores for Task 2 are: ", scores2)
print("Brier Scores for Task 3 are: ", scores3)
