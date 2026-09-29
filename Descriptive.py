import pandas as pd

class Descriptive():

    def __init__(self):
        pass

    def segreQuanQual(self, dataset):
        quantative = []
        qualtative = []

        for i in dataset.columns:
            if dataset[i].dtype == 'object':
                qualtative.append(i)
            else:
                quantative.append(i)

        print("The Quantitative Data:", quantative)
        print("The Qualitative Data:", qualtative)

        return quantative, qualtative


    def descriptive_Analysis(self, dataset, quantative):

        des_data = pd.DataFrame(
            index=[
                "Count", "Mean", "Median", "Mode", "Std", "Min",
                "Q1:25%", "Q2:50%", "Q3:75%", "Q4:100%",
                "IQR", "1.5Rule", "Lesser", "Greater"
            ],
            columns=quantative
        )

        for i in quantative:

            des_data.loc["Count", i] = len(dataset[i])
            des_data.loc["Mean", i] = dataset[i].mean()
            des_data.loc["Median", i] = dataset[i].median()
            des_data.loc["Mode", i] = dataset[i].mode().iloc[0]
            des_data.loc["Std", i] = dataset[i].std()
            des_data.loc["Min", i] = dataset[i].min()

            des_data.loc["Q1:25%", i] = dataset[i].quantile(0.25)
            des_data.loc["Q2:50%", i] = dataset[i].quantile(0.50)
            des_data.loc["Q3:75%", i] = dataset[i].quantile(0.75)
            des_data.loc["Q4:100%", i] = dataset[i].max()

            des_data.loc["IQR", i] = (
                des_data.loc["Q3:75%", i]
                - des_data.loc["Q1:25%", i]
            )

            des_data.loc["1.5Rule", i] = (
                1.5 * des_data.loc["IQR", i]
            )

            des_data.loc["Lesser", i] = (
                des_data.loc["Q1:25%", i]
                - des_data.loc["1.5Rule", i]
            )

            des_data.loc["Greater", i] = (
                des_data.loc["Q3:75%", i]
                + des_data.loc["1.5Rule", i]
            )

        return des_data


    def outliercolumn(self, quantative, des_data):

        lesser = []
        greater = []

        for i in quantative:

            if des_data.loc["Lesser", i] > des_data.loc["Min", i]:
                lesser.append(i)

            if des_data.loc["Greater", i] < des_data.loc["Q4:100%", i]:
                greater.append(i)

        print("Lesser Range:", lesser)
        print("Greater Range:", greater)

        return lesser, greater


    def changeoutlier(self, dataset, des_Data, lesser, greater):

        for i in lesser:
            dataset.loc[
                dataset[i] < des_Data.loc["Lesser", i], i
            ] = des_Data.loc["Lesser", i]

        for j in greater:
            dataset.loc[
                dataset[j] > des_Data.loc["Greater", j], j
            ] = des_Data.loc["Greater", j]

        return dataset