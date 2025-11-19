from decimal import Decimal
from collections import Counter
import pandas as pd
import numpy as np

from helper_funcs import gate_check

age_gates = [13,16,18]
abbrev_lookup = {"AE": "Estimation", "AV": "Verification", "AI": "Inference"}
rev_abbrev_lookup = {abbrev_lookup[abbr]: abbr for abbr in abbrev_lookup}

def cleansed_filter_by_method(df, discard_ae_outliers=True, method=None):

    if method in rev_abbrev_lookup:
        df = df[df["METHOD"] == method]
    else:
        raise AssertionError("No method selected")

    overall_abs_error_mean = df['ABS_ERROR'].astype('float').agg('mean')
    overall_abs_error_stdev = df['ABS_ERROR'].astype('float').agg('std')

    if discard_ae_outliers:
        # erase abs_error entries for those with absolute error outside 2 standard deviation
        new_abs_error_col = df['ABS_ERROR'].apply(
            lambda x: 
                x if pd.notna(x) 
                    and x < overall_abs_error_mean+2*overall_abs_error_stdev 
                    and x > overall_abs_error_mean-2*overall_abs_error_stdev 
                else None
            )
        df['ABS_ERROR'] = new_abs_error_col

    return df

def generate_check_age_gates(df, age_gates, method=None):
    if method not in rev_abbrev_lookup:
        raise AssertionError("No method selected")

    for age_gate in age_gates:
        colname = f"CHECK{age_gate}"
        df[colname] = df.apply(
            lambda x: gate_check(
                x['SUBJECT_AGE'],
                x[f"{rev_abbrev_lookup[method]}_RESULT"],
                age_gate if x['AGE_GATE'] == 0 else x['AGE_GATE']
            ) if (x['AGE_GATE'] == 0 or x['AGE_GATE'] == age_gate) else None,
            axis=1,
            result_type='reduce'
        )
    df.drop(columns=["AGE_GATE"], inplace=True)

    return df

def calc_accuracy(tally):
    tp = tally.get('TP', 0)
    tn = tally.get('TN', 0)
    fp = tally.get('FP', 0)
    fn = tally.get('FN', 0)

    r = {
        "samples": tp+tn+fp+fn,
        "accuracy": round((tp+tn) / (tp+tn+fp+fn), 4)*100 if tp+tn+fp+fn > 0 else None,
        "FPR": round((fp) / (tn+fp), 4)*100 if tn+fp > 0 else None,
        "FNR": round((fn) / (tp+fn), 4)*100 if tp+fn > 0 else None,
        "TPR": round((tp) / (tp+fn), 4)*100 if tp+fn > 0 else None,
        "TNR": round((tn) / (tn+fp), 4)*100 if tn+fp > 0 else None
    }
    return r

def group_aggregate(groupby_columns, df, stack_method="long"):

    def combine_all_age_gate_check(row):
        counter_sum = Counter()
        for age_gate in age_gates:
            age_gate_check = row[f"CHECK{age_gate}"]
            if type(age_gate_check) is Counter:
                counter_sum += age_gate_check
        return counter_sum

    if len(groupby_columns) == 0:
        samples = df['SUBJECT_ID'].count()
        grouped_mean_abs_error = np.mean(df['ABS_ERROR'])
        grouped_mean_abs_dev = np.std(df['ABS_ERROR'])
        #grouped_median_verification_time = np.median(df['verification_time'])

        age_gate_accuracy = {age_gate: calc_accuracy(Counter(df[f"CHECK{age_gate}"])) for age_gate in age_gates}

        age_gate_mean_abs_error = {age_gate: df[pd.notna(df[f"CHECK{age_gate}"])]["ABS_ERROR"].agg('mean') for age_gate in age_gates}
        age_gate_mean_abs_dev = {age_gate: df[pd.notna(df[f"CHECK{age_gate}"])]["ABS_ERROR"].agg('std') for age_gate in age_gates}

        grouped_df = pd.DataFrame.from_records([{
            "Samples": samples,
            "Mean absolute error" :grouped_mean_abs_error,
            "Absolute error standard deviation": grouped_mean_abs_dev,
            #"Median verification time": grouped_median_verification_time,
            **{f"AG{age_gate} samples": age_gate_accuracy[age_gate]["samples"] for age_gate in age_gate_accuracy},
            **{f"AG{age_gate} accuracy": age_gate_accuracy[age_gate]["accuracy"] for age_gate in age_gate_accuracy},
            **{f"AG{age_gate} False Positive Rate": age_gate_accuracy[age_gate]["FPR"] for age_gate in age_gate_accuracy},
            **{f"AG{age_gate} False Negative Rate": age_gate_accuracy[age_gate]["FNR"] for age_gate in age_gate_accuracy},
            **{f"AG{age_gate} True Positive Rate": age_gate_accuracy[age_gate]["TPR"] for age_gate in age_gate_accuracy},
            **{f"AG{age_gate} True Negative Rate": age_gate_accuracy[age_gate]["TNR"] for age_gate in age_gate_accuracy},
            **{f"AG{age_gate} mean absolute error": age_gate_mean_abs_error[age_gate] for age_gate in age_gate_mean_abs_error},
            **{f"AG{age_gate} absolute error stdev": age_gate_mean_abs_dev[age_gate] for age_gate in age_gate_mean_abs_dev}
        }], index=[""])


    else:
        group_func = df.groupby(groupby_columns, dropna=False)
        grouped_df = group_func.agg(Counter)

        grouped_df['SAMPLES'] = group_func['SUBJECT_ID'].count()
        grouped_mean_abs_error = group_func['ABS_ERROR'].agg('mean')
        grouped_mean_abs_dev = group_func['ABS_ERROR'].agg('std')

        if 'VERIFICATION_TIME' in df.columns:
            grouped_df['MEDIAN_VERIFICATION_TIME'] = group_func['VERIFICATION_TIME'].agg('median')
        if 'CONFIDENCE_LEVEL' in df.columns:
            age_gate_median_confidence = {
                age_gate: df[pd.notna(df[f"CONFIDENCE_LEVEL"])].groupby(groupby_columns, dropna=False)["CONFIDENCE_LEVEL"].agg('median').apply(lambda x: round(x, 2))
                    for age_gate in age_gates
            }

        overall_accuracy = grouped_df.apply(lambda x: combine_all_age_gate_check(x), axis=1, result_type='reduce').apply(calc_accuracy)

        age_gate_accuracy = {age_gate: grouped_df[f"CHECK{age_gate}"].apply(calc_accuracy) for age_gate in age_gates}
        
        age_gate_mean_abs_error = {
            age_gate: df[pd.notna(df[f"CHECK{age_gate}"])].groupby(groupby_columns, dropna=False)["ABS_ERROR"].agg('mean').apply(lambda x: round(x, 2))
            for age_gate in age_gates
        }
        age_gate_abs_error_stdev = {
            age_gate: df[pd.notna(df[f"CHECK{age_gate}"])].groupby(groupby_columns, dropna=False)["ABS_ERROR"].agg('std').apply(lambda x: round(x, 2))
            for age_gate in age_gates
        }

        if stack_method == "wide":
            """
            for age_gate in age_gate_accuracy:
                grouped_df[f"AG{age_gate} samples"] = age_gate_accuracy[age_gate].apply(lambda x: x["samples"])
                grouped_df[f"AG{age_gate} accuracy"] = age_gate_accuracy[age_gate].apply(lambda x: x["accuracy"])
                grouped_df[f"AG{age_gate} FPR"] = age_gate_accuracy[age_gate].apply(lambda x: x["FPR"])
                grouped_df[f"AG{age_gate} FNR"] = age_gate_accuracy[age_gate].apply(lambda x: x["FNR"])
                grouped_df[f"AG{age_gate} TPR"] = age_gate_accuracy[age_gate].apply(lambda x: x["TPR"])
                grouped_df[f"AG{age_gate} TNR"] = age_gate_accuracy[age_gate].apply(lambda x: x["TNR"])
            
            for age_gate in age_gate_mean_abs_error:
                grouped_df[f"AG{age_gate} MAE"] = age_gate_mean_abs_error[age_gate]
            for age_gate in age_gate_abs_error_stdev:
                grouped_df[f"AG{age_gate} absolute error stdev"] = age_gate_abs_error_stdev[age_gate]
            """

            for ag in age_gates:
                df[f"check abs_error age gate {ag}"] = df.apply(
                    lambda x: (x[f"check age gate {ag}"], x["abs_error"] if pd.notna(x["abs_error"]) else np.nan),
                    axis = 1
                )
            
            df_grouped = df.groupby(groupby_columns, dropna=False)
            result_df = pd.DataFrame()

            for ag in age_gates:
                df_grouped_gate_list_agg = df_grouped[f"check abs_error age gate {ag}"].agg(list)
                df_grouped_gate_check = df_grouped_gate_list_agg.apply(lambda x: Counter([e[0] for e in x]))
                df_grouped_gate_accuracy = df_grouped_gate_check.apply(calc_accuracy)

                for key in ["samples","accuracy","FPR","FNR","TPR","TNR"]:
                    result_df[(ag, key)] = df_grouped_gate_accuracy.apply(lambda x: x[key])

                df_grouped_gate_mae = df_grouped_gate_list_agg.apply(lambda x: np.mean([e[1] for e in x]))
                df_grouped_gate_ae_stdev = df_grouped_gate_list_agg.apply(lambda x: np.std([e[1] for e in x]))    

                result_df[(ag, "MAE")] = df_grouped_gate_mae
                result_df[(ag, "absolute error stdev")] = df_grouped_gate_ae_stdev          

            grouped_df['Mean absolute error'] = grouped_mean_abs_error.map(lambda x: None if np.isnan(x) else round(x, 2))
            grouped_df['Absolute error standard deviation'] = grouped_mean_abs_dev.map(lambda x: None if np.isnan(x) else round(x, 2))
            grouped_df['Overall accuracy'] = overall_accuracy.map(lambda x: x['accuracy'])
        
            subfields = [
                "samples",
                "FPR",
                "FNR",
                "TPR",
                "TNR",
                "accuracy",
                "MAE",
                "absolute_error_stdev",
            ]

            select_columns = [
                'Samples',
                *[f"AG{age_gate} {field}" for age_gate in age_gates for field in subfields],
                'Mean absolute error',
                'Absolute error standard deviation',
                'Overall accuracy'
            ]
            if 'verification_time' in df.columns:
                select_columns.append('median_verification_time')
            
            display_df = grouped_df[select_columns]
            return display_df
        
        if stack_method == "long":
            
            #df["i"] = df.index
            #df_long = pd.wide_to_long(df, "check", i="i", j="age_gate")
            
            df_long = pd.melt(df, id_vars=groupby_columns, value_vars=[f"CHECK{ag}" for ag in age_gates], ignore_index=False)

            df_long["AGE_GATE"] = df_long["variable"].apply(lambda x: int(x.lstrip("CHECK")))
            df_long["ABS_ERROR"] = df["ABS_ERROR"]

            if 'VERIFICATION_TIME' in df.columns:
                df_long["VERIFICATION_TIME"] = df["VERIFICATION_TIME"]

            df_long_grouped = df_long.groupby(['AGE_GATE']+groupby_columns, dropna=False)
            df_long_grouped_list_agg = df_long_grouped['value'].agg(Counter)
            df_long_grouped_accuracy = df_long_grouped_list_agg.apply(calc_accuracy)
            
            df_long_grouped_mae = df_long_grouped["ABS_ERROR"].agg('mean')
            df_long_grouped_ae_stdev = df_long_grouped["ABS_ERROR"].agg('std')
            
            result_df = pd.DataFrame()
            for key in ["samples","accuracy","FPR","FNR","TPR","TNR"]:
                result_df[key] = df_long_grouped_accuracy.apply(lambda x: x[key])
            
            result_df["MAE"] = df_long_grouped_mae
            result_df["ABSOLUTE_ERROR_STDEV"] = df_long_grouped_ae_stdev

            select_columns = [
                "samples",
                "FPR",
                "FNR",
                "TPR",
                "TNR",
                "accuracy",
                "MAE",
                "ABSOLUTE_ERROR_STDEV"
            ]

            if 'VERIFICATION_TIME' in df.columns:
                result_df["MEDIAN_VERIFICATION_TIME"] = df_long_grouped["VERIFICATION_TIME"].agg('median')
                select_columns.append("MEDIAN_VERIFICATION_TIME")
            
            display_df = result_df[select_columns]
            
            return display_df