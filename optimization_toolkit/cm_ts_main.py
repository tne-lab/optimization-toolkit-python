import os
import numpy as np
import optimization_toolkit.cm_ts_setupdata as cm_ts_setupdata
import optimization_toolkit.ts_function_ensemble as ts_function_ensemble
import optimization_toolkit.ts_datafetcher as ts_datafetcher
seed_value = 1  # Set your desired seed value
np.random.seed(seed_value)
def cm_ts_main():
    # Initialize data storage
    data1 = {}

    # Perform simulations for different parameters
    for NTrials in [600]:
        for dst in ["noalgorithm"]:
            for test in [1]:
                for divisor in [15]:
                    for model in range(2, 9, 2):
                        print(f"{dst}-{divisor}-{model}-Started")
                        vL = cm_ts_setupdata({},1, NTrials, divisor, 1, model, test, dst)
                        expV = ts_function_ensemble(vL)
                        data1 = ts_datafetcher(expV, vL, model=model, data1=data1)
                        # Save data
                        save_file = f'D:/Sumedh/{dst}{model}4days'
                        np.save(save_file, data1)
                        data1 = {}

    # Calculate elapsed time
    k = 0  # Placeholder for elapsed time
    return data1, k


# Define other necessary functions (cm_ts_setupdata, ts_function_ensemble, ts_datafetcher)

# Call the main function
if __name__ == "__main__":
    cm_ts_main()
