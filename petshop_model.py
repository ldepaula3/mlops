import sys
import numpy
import pandas
import pickle
from sklearn.preprocessing import OneHotEncoder

def preprocessing(df, ohe_loc = None):
    df["Pure_Breed"] = df["Pure_Breed"].astype(str).str.upper() 
    df["Pure_Breed"] = df["Pure_Breed"].eq("YES").mul(1).values

    df["Animal_Type_New"] = df["Animal_Type_New"].astype(str).str.upper() 
    df["Animal_Type_New"] = df["Animal_Type_New"].eq("DOG").mul(1).values
    
    encode_cols = df.select_dtypes(include=["object"]).columns.tolist()
    
    with open(ohe_loc, "rb") as ohe_file:
        ohe = pickle.load(ohe_file) 
    enc = ohe.transform(df[encode_cols])
    df[ohe.get_feature_names(encode_cols).tolist()] = pandas.DataFrame(enc, index=df.index)

    df.drop(encode_cols,1,inplace=True)
    df.dropna(inplace=True)
    
    return df

#inside input parameter goes all the predictor/input variables
def scoreModel(Age_Group_Intake, Animal_Type_New, Color_Group, Intake_Condition, Pure_Breed, Season, Sex, Sterilized_Time, Intake_Type, Month_of_Intake):
    "Output: EM_EVENTPROBABILITY"
    try:
        _pFile = open( "petshop_model.pickle", "rb")
        _thisModelFit = pickle.load(_pFile)
        _pFile.close()

        # Construct the input array for scoring (the first term is for the Intercept)
        # mapyour input parameters with associated column names in pandas table
        input_array = pandas.DataFrame([[Age_Group_Intake, Animal_Type_New, Color_Group, Intake_Condition, Pure_Breed, Season, Sex, Sterilized_Time, Intake_Type, Month_of_Intake]],

                                       columns = ["Age_Group_Intake", "Animal_Type_New", "Color_Group", "Intake_Condition", "Pure_Breed", "Season", "Sex", "Sterilized_Time", "Intake_Type", "Month_of_Intake"], 
                                       dtype = float)


        # custom preprocessing step
        input_array = preprocessing(input_array, ohe_loc = "encoder.pickle")

        # perform the same preprocessing procedure as it was done during training
        input_array.fillna(input_array.mean(), inplace=True)

        # Calculate the predicted probabilities
        _predProb = _thisModelFit.predict(input_array)

        # Retrieve the event probability
        EM_EVENTPROBABILITY = float(_predProb[0])

        return EM_EVENTPROBABILITY
    except Exception as e:
        print(e)
        return float(-1)
    
def main():
    # print command line arguments
    print(" The probability is: " + str(scoreModel(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8],sys.argv[9],sys.argv[10])))


if __name__ == "__main__":
    main()

