import sensor_data_model


def create_sensor_model():
    locGen = r"D:\Sumedh\Projects\Methods for psychiatric DBS programming\Data\Simulated"
    sensor_data_path = r"D:\Sumedh\Projects\Methods for psychiatric DBS programming\Data\sensor_HigherWk"

    # Add path to the MATLAB toolbox (not required in Python)
    # MATLAB's `addpath` command is not necessary in Python

    for i in range(1, 7):
        for k in range(1, 176):
            sensor_data_model(k, i, 1, sensor_data_path, locGen)
