import pandas as pd

df = pd.read_csv('C:/Users/ROXANA CASTILLO/Desktop/354/gym_members_exercise_tracking.csv')

def convertir_a_arff(df, nombre_archivo_arff):
    with open(nombre_archivo_arff, 'w') as f:
        f.write(f"@RELATION gym_members_exercise_tracking\n\n")
        for column in df.columns:
            if df[column].dtype == 'object':
                unique_values = df[column].unique()
                unique_values_str = ','.join([str(v) for v in unique_values])
                f.write(f"@ATTRIBUTE {column} {{{unique_values_str}}}\n")
            else:
                f.write(f"@ATTRIBUTE {column} NUMERIC\n")
        f.write("\n@DATA\n")
        for index, row in df.iterrows():
            row_str = ','.join([str(val) for val in row])
            f.write(f"{row_str}\n")


convertir_a_arff(df, 'C:/Users/ROXANA CASTILLO/Desktop/354/gym_members_exercise_tracking.arff')


def onehot_encoder_manual(df, column):
    unique_values = df[column].unique()
    encoded_columns = pd.DataFrame()

    for unique_value in unique_values:
        encoded_columns[f'{column}_{unique_value}'] = df[column].apply(lambda x: 1 if x == unique_value else 0)

    return encoded_columns


df_onehot = onehot_encoder_manual(df, 'Workout_Type')
df = pd.concat([df, df_onehot], axis=1)
df.drop(columns=['Workout_Type'], inplace=True)


def label_encoder_manual(df, column):
    unique_values = df[column].unique()
    label_map = {value: idx for idx, value in enumerate(unique_values)}
    df[column] = df[column].map(label_map)
    return df


df = label_encoder_manual(df, 'Experience_Level')


def discretize_manual(df, column, bins):
    df[f'{column}_Discretized'] = pd.cut(df[column], bins=bins, labels=False)
    return df


df = discretize_manual(df, 'Age', 3)


def normalize_manual(df, columns):
    for column in columns:
        min_value = df[column].min()
        max_value = df[column].max()
        df[column] = (df[column] - min_value) / (max_value - min_value)
    return df


df = normalize_manual(df, ['Weight (kg)', 'Height (m)', 'BMI'])

df.head()
