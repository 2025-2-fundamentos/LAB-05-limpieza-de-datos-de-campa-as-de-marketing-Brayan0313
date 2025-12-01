"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


"""
Escriba el codigo que ejecute la accion solicitada.
"""
import pandas as pd
import zipfile
from pathlib import Path
import os
import glob
# pylint: disable=import-outside-toplevel

def load_input(input):

    dataframes = []

    input_folder = Path(input)

    for archivo in input_folder.iterdir():

        with zipfile.ZipFile(archivo) as zip_file:
                for csv_file in zip_file.namelist():
                    with zip_file.open(csv_file) as file:
                        df = pd.read_csv(file)
                        dataframes.append(df)
    
    dataframe = pd.concat(dataframes, ignore_index=True)

    return dataframe

def save_output(dataframe1, dataframe2, dataframe3, output_directory, output_name1, output_name2, output_name3):
    """Save output to a file."""

    if os.path.exists(output_directory):
        files = glob.glob(f"{output_directory}/*")
        for file in files:
            os.remove(file)
        os.rmdir(output_directory)

    os.makedirs(output_directory)

    dataframe1.to_csv(
        f"{output_directory}/{output_name1}",
        sep=",",
        index=False,
        header=True,
    )
    dataframe2.to_csv(
        f"{output_directory}/{output_name2}",
        sep=",",
        index=False,
        header=True,
    )

    dataframe3.to_csv(
        f"{output_directory}/{output_name3}",
        sep=",",
        index=False,
        header=True,
    )



def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    df = load_input('files/input')
    #cleaning data from df

    #cambios en la columna 'job'
    df['job'] = df['job'].str.replace('.','', regex=False).str.replace('-','_', regex=False)

    #cambios en la columna education
    df['education'] = df['education'].str.replace('.','_', regex=False)
    df['education'] = df['education'].replace('unknown',pd.NA)

    #cambios en la columna credit_default
    df['credit_default'] = df['credit_default'].replace('yes',1, regex=False)
    df.loc[df['credit_default'] != 1, 'credit_default'] = 0

    #cambios en la columna mortgage
    df['mortgage'] = df['mortgage'].replace('yes',1, regex=False)
    df.loc[df['mortgage'] != 1, 'mortgage'] = 0

    #cambios en previous_outcome
    df['previous_outcome'] = df['previous_outcome'].replace('success',1)
    df.loc[df['previous_outcome'] != 1, 'previous_outcome'] = 0

    #cambios en campaign_outcome
    df['campaign_outcome'] = df['campaign_outcome'].replace('yes',1)
    df.loc[df['campaign_outcome'] != 1, 'campaign_outcome'] = 0

    #creacion de last_contact_day
    meses_a_numeros = {
    'mar': '03',
    'apr': '04',
    'may': '05',
    'jun': '06',
    'jul': '07',
    'aug': '08',
    'sep': '09',
    'oct': '10',
    'nov': '11',
    'dec': '12'
    }

    df['month'] = df['month'].map(meses_a_numeros)
    df['last_contact_date'] = '2022' + '-' + df['month'] + '-' + df['day'].astype(str)

    #crear los 3 df
    client_df = df.iloc[:, 1:8 ]

    campaign_df = df.iloc[:, [1,10,11,12,13,16,17]]

    economics_df = df.iloc[:, [1,14,15]]

    save_output(client_df, campaign_df, economics_df, 'files/output', 'client.csv', 'campaign.csv', 'economics.csv')


if __name__ == "__main__":
    clean_campaign_data()