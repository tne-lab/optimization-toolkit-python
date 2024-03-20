def ts_datafetcher(expV, vL, model, data1):
    data1[f"test{vL['test']}_divisor{vL['divisor']}_model{model}"] = expV
    return data1
