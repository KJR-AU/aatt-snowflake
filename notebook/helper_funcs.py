import math
import bisect
import json
import numpy as np
import pandas as pd

age_gates = [13,16,18]

def age_bucket(age):
    age_integers = list(range(10,26))
    i = bisect.bisect_right(age_integers, age)
    if i == 0:
        return f"<{age_integers[0]}"
    elif i < len(age_integers):
        if age_integers[i-1] == age_integers[i]-1:
            return f"{age_integers[i-1]}"
        else:
            return f"{age_integers[i-1]}-{age_integers[i]-1}"
    else:
        return f">={age_integers[-1]}"


def gate_check(real_age, estimated_age, age_gate):
    
    def positive_check(query, threshold):
        return "TP" if query >= threshold else "FP"
    
    def negative_check(query, threshold):
        return "TN" if query < threshold else "FN"
    
    try:
        if type(real_age) is str:
            if real_age.startswith(">="):
                real_age = float(real_age[2:])
            elif real_age.startswith("<"):
                real_age = float(real_age[1:])
            else:
                real_age = pd.to_numeric(real_age, errors='raise', downcast='float')
        else:
            real_age = pd.to_numeric(real_age, errors='raise', downcast='float')
    except:
        return None

    try:
        if pd.isna(estimated_age):
            return None
        estimated_age_float = pd.to_numeric(estimated_age, errors='raise', downcast='float')
        
        if estimated_age_float >= age_gate:
            check = positive_check(real_age, age_gate)
        else:
            check = negative_check(real_age, age_gate)
        return check

    # generally for handling cases where estimated age is not a number, but only string that is a binary choice of over/under some integer e.g. "over 18"
    except:
        split_str = estimated_age.split(' ')
        if age_gate == int(split_str[1]):
            if split_str[0] == "over":
                if real_age >= age_gate:
                    return "TP"
                else:
                    return "FP"
            elif split_str[0] == "under":
                if real_age < age_gate:
                    return "TN"
                else:
                    return "FN"
        else:
            return None

def standardise_age_check(age_gate, estimated_age, age_gate_checks):
    if pd.notna(age_gate_checks):
        return age_gate_checks
    else:
        if np.isnan(estimated_age):
            return None
        elif ~np.isnan(age_gate):
            if age_gate != 0:
                return {age_gate: estimated_age >= age_gate}
            else:
                return {ag: estimated_age >= ag for ag in age_gates}
        else:
            return None

def expand_gate(real_age, age_checks_list, abs_error, age_gate, abs_err_lower_bound=-math.inf, abs_err_upper_bound=math.inf):

    # enabling this will not process rows with absolute error outside bounds (i.e. outliers)
    # in effect, no TP,TN,FP,FN will be calculated for that row
    # leave commented if returned estimated age is an outlier but if it can still be considered valid age gate check (e.g. older than 13, older than 16, etc)
    #if not np.isnan(abs_error):
    #    if abs_error < abs_err_lower_bound or abs_error > abs_err_upper_bound:
    #        return None

    if pd.notna(age_checks_list):

        age_truth_check = age_checks_list.get(age_gate, None)
        if age_truth_check == True:
            if real_age >= age_gate:
                return "TP"
            else:
                return "FP"
        elif age_truth_check == False:
            if real_age < age_gate:
                return "TN"
            else:
                return "FN"
        else:
            return None

def fill_subject_background(first_nations, country_of_birth, country_of_birth_father, country_of_birth_mother):
    def parents_background_check(first_nations, country_of_birth, country_of_birth_father, country_of_birth_mother):
        if first_nations in ["aboriginal", "torresStrait", "both"]:
            return "First Nations"
        else:
            if pd.isna(country_of_birth_father):
                country_of_birth_father = "none"
            if pd.isna(country_of_birth_mother):
                country_of_birth_mother = "none"

            if country_of_birth_father.lower() == country_of_birth_mother.lower():
                if country_of_birth_father.lower() != "none":
                    return country_of_birth_father
                else:
                    if country_of_birth.lower() != "none":
                        return country_of_birth
                    else:
                        return "Unknown"
            else:
                if country_of_birth_father.lower() == "none":
                    return country_of_birth_mother
                else:
                    return country_of_birth_father
        return None # should never get here

    country_region_num = json.load(open("country_region_num.json","r"))
    region_name = json.load(open("region_name.json","r"))

    parents_bg = parents_background_check(first_nations, country_of_birth, country_of_birth_father, country_of_birth_mother)
    
    if parents_bg == "First Nations":
        return parents_bg
    elif parents_bg in country_region_num and country_region_num[parents_bg] != 0 and country_region_num[parents_bg] in region_name:
        return region_name[country_region_num[parents_bg]]
    else:
        return "Unknown"