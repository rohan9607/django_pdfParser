import json
import re
from PyPDF2 import PdfReader

two_numbers_pattern = "([-+]?[0-9]*\.[0-9]+)"
right_dash_number_pattern = "([-+]?[0-9]*\.[0-9]+)\s[-]"
left_dash_number_pattern = "[-]\s([-+]?[0-9]*\.[0-9]+)"
def pdfParser(uploaded_file):
    file = PdfReader(uploaded_file)
    i = 0
    parser_count = 0
    jsonData = {
        "to_year": {
            "year": None,
            "assets": {
                "non_current_assets": {
                    "property_plant_equipments": None,
                    "goodwill": None,
                    "other_intangible_assets": None,
                    "financial_assets": {
                        "investments": None,
                        "other_financial_assets": None
                    }
                },
                "current_assets": {
                    "financial_assets": {
                        "trade_receivables": None,
                        "cash_and_equivalents": None,
                        "loans_and_advances": None
                    },
                    "other_current_assets": None
                }
            },
            "equities_liabilities": {
                "equities": {
                    "share_capital": None,
                    "other_capital": None
                },
                "liabilities": {
                    "non_current_liabilities": {
                        "financial_liabilities": {
                            "borrowings": None,
                            "lease_liabilities": None,
                        },
                        "provisions": None
                    },
                    "current_liabilities": {
                        "financial_liabilities": {
                            "borrowings": None,
                            "lease_liabilities": None,
                            "trade_payables": {
                                "total_outstanding_dues_of_micro_enterprises_and_small_enterprises": None,
                                "total outstanding dues of creditors other than micro enterprises and small enterprises": None,
                            },
                            "others_financial_liabilities": None
                        },
                        "provisions": None,
                        "other_current_liabilities": None
                    }
                }
            }
        },
        "from_year": {
            "year": None,
            "assets": {
                "non_current_assets": {
                    "property_plant_equipments": None,
                    "goodwill": None,
                    "other_intangible_assets": None,
                    "financial_assets": {
                        "investments": None,
                        "other_financial_assets": None
                    }
                },
                "current_assets": {
                    "financial_assets": {
                        "trade_receivables": None,
                        "cash_and_equivalents": None,
                        "loans_and_advances": None
                    },
                    "other_current_assets": None
                }
            },
            "equities_liabilities": {
                "equities": {
                    "share_capital": None,
                    "other_capital": None
                },
                "liabilities": {
                    "non_current_liabilities": {
                        "financial_liabilities": {
                            "borrowings": None,
                            "lease_liabilities": None,
                        },
                        "provisions": None
                    },
                    "current_liabilities": {
                        "financial_liabilities": {
                            "borrowings": None,
                            "lease_liabilities": None,
                            "trade_payables": {
                                "total_outstanding_dues_of_micro_enterprises_and_small_enterprises": None,
                                "total outstanding dues of creditors other than micro enterprises and small enterprises": None,
                            },
                            "others_financial_liabilities": None
                        },
                        "provisions": None,
                        "other_current_liabilities": None
                    }
                }
            }
        }
    }

    for page in file.pages:
        text = page.extract_text()
        if re.search("Balance\s+sheet\s+as\s+at ", text):
            parser_count  = 1
            splittedText1 = []
            splittedText = []
            for t in text.splitlines():
                newT = t.strip()
                newT = newT.rstrip()
                newT = newT.lstrip()
                splittedText1.append(newT)
            for t in splittedText1:
                splt_arr = t.split()
                refinedText = ""
                for w in splt_arr:
                    newS = w.strip()
                    newS = newS.lstrip()
                    newS = newS.rstrip()
                    refinedText += newS + " "
                splittedText.append(refinedText.strip())
            line_index = 0
            for line in splittedText:
                if re.search("Notes", line):
                    extract_year = re.findall("\d{1,2}\s+[a-zA-Z]+\s+\d{4}", line)
                    to_year = extract_year[0]
                    from_year = extract_year[1]
                    jsonData["to_year"]["year"] = to_year
                    jsonData["from_year"]["year"] = from_year
                    break

            # Assets
            asset_index = splittedText.index("ASSETS")
            asset_index_counter = asset_index
            # Non Current Assets
            for non_crnt_asset_element in splittedText[asset_index:]:
                if re.search("Current assets", non_crnt_asset_element):
                    break
                #     Property, plant and equipments
                if re.search("Property, plant and equipments", non_crnt_asset_element):
                    p_values = re.findall(two_numbers_pattern, non_crnt_asset_element)
                    if (len(p_values) > 1):
                        jsonData["to_year"]["assets"]["non_current_assets"]["property_plant_equipments"] = p_values[0]
                        jsonData["from_year"]["assets"]["non_current_assets"]["property_plant_equipments"] = p_values[1]
                    p_values = re.findall(left_dash_number_pattern, non_crnt_asset_element)
                    if len(p_values) == 1:
                        jsonData["from_year"]["assets"]["non_current_assets"]["property_plant_equipments"] = p_values[1]
                    p_values = re.findall(right_dash_number_pattern, non_crnt_asset_element)
                    if len(p_values) == 1:
                        jsonData["to_year"]["assets"]["non_current_assets"]["property_plant_equipments"] = p_values[0]

                # GoodWill
                if re.search("Goodwill", non_crnt_asset_element):
                    p_values = re.findall(two_numbers_pattern, non_crnt_asset_element)
                    if (len(p_values) > 1):
                        jsonData["to_year"]["assets"]["non_current_assets"]["goodwill"] = p_values[0]
                        jsonData["from_year"]["assets"]["non_current_assets"]["goodwill"] = p_values[1]
                    p_values = re.findall(left_dash_number_pattern, non_crnt_asset_element)
                    if len(p_values) == 1:
                        jsonData["from_year"]["assets"]["non_current_assets"]["goodwill"] = p_values[1]

                    p_values = re.findall(right_dash_number_pattern, non_crnt_asset_element)
                    if len(p_values) == 1:
                        jsonData["to_year"]["assets"]["non_current_assets"]["goodwill"] = p_values[0]

                #         Other intangible asstes
                if re.search("Other Intangible assets", non_crnt_asset_element):
                    p_values = re.findall(two_numbers_pattern, non_crnt_asset_element)
                    if (len(p_values) > 1):
                        jsonData["to_year"]["assets"]["non_current_assets"]["other_intangible_assets"] = p_values[0]
                        jsonData["from_year"]["assets"]["non_current_assets"]["other_intangible_assets"] = p_values[1]
                    p_values = re.findall(left_dash_number_pattern, non_crnt_asset_element)
                    if len(p_values) == 1:
                        jsonData["from_year"]["assets"]["non_current_assets"]["other_intangible_assets"] = p_values[1]

                    p_values = re.findall(right_dash_number_pattern, non_crnt_asset_element)
                    if len(p_values) == 1:
                        jsonData["to_year"]["assets"]["non_current_assets"]["other_intangible_assets"] = p_values[0]

                if re.search("Financial assets", non_crnt_asset_element):
                    for fs in splittedText[asset_index_counter + 1:]:
                        if re.search("Current assets", fs):
                            break
                        if re.search("Investments", fs):
                            p_values = re.findall(two_numbers_pattern, fs)
                            if (len(p_values) > 1):
                                jsonData["to_year"]["assets"]["non_current_assets"]["financial_assets"]["investments"] = \
                                    p_values[0]
                                jsonData["from_year"]["assets"]["non_current_assets"]["financial_assets"]["investments"] = \
                                    p_values[
                                        1]
                            p_values = re.findall(left_dash_number_pattern, fs)
                            if len(p_values) == 1:

                                jsonData["from_year"]["assets"]["non_current_assets"]["financial_assets"]["investments"] = \
                                    p_values[1]

                            p_values = re.findall(right_dash_number_pattern, fs)
                            if len(p_values) == 1:
                                jsonData["to_year"]["assets"]["non_current_assets"]["financial_assets"]["investments"] = \
                                    p_values[0]

                        if re.search("Other financial assets", fs):
                            p_values = re.findall(two_numbers_pattern, fs)
                            if (len(p_values) > 1):
                                jsonData["to_year"]["assets"]["non_current_assets"]["financial_assets"][
                                    "other_financial_assets"] = p_values[0]
                                jsonData["from_year"]["assets"]["non_current_assets"]["financial_assets"][
                                    "other_financial_assets"] = p_values[
                                    1]
                            p_values = re.findall(left_dash_number_pattern, fs)
                            if len(p_values) == 1:

                                jsonData["from_year"]["assets"]["non_current_assets"]["financial_assets"][
                                    "other_financial_assets"] = p_values[1]

                            p_values = re.findall(right_dash_number_pattern, fs)
                            if len(p_values) == 1:
                                jsonData["to_year"]["assets"]["non_current_assets"]["financial_assets"][
                                    "other_financial_assets"] = p_values[0]

                asset_index_counter += 1

            #     Current Assets
            current_assets_start_idx = splittedText.index("Current assets")
            current_assets_counter = current_assets_start_idx
            for crnt_asset_element in splittedText[current_assets_start_idx:]:
                if re.search("TOTAL ASSETS", crnt_asset_element):
                    break
                if re.search("Financial assets", crnt_asset_element):
                    for fs in splittedText[current_assets_counter + 1:]:
                        if re.search("TOTAL ASSETS", fs):
                            break
                        if re.search("Trade receivables", fs):
                            p_values = re.findall(two_numbers_pattern, fs)
                            if (len(p_values) > 1):
                                jsonData["to_year"]["assets"]["current_assets"]["financial_assets"]["trade_receivables"] = \
                                    p_values[0]
                                jsonData["from_year"]["assets"]["current_assets"]["financial_assets"]["trade_receivables"] = \
                                    p_values[
                                        1]
                            p_values = re.findall(left_dash_number_pattern, fs)
                            if len(p_values) == 1:
                                jsonData["from_year"]["assets"]["current_assets"]["financial_assets"]["trade_receivables"] = \
                                    p_values[1]

                            p_values = re.findall(right_dash_number_pattern, fs)
                            if len(p_values) == 1:
                                jsonData["to_year"]["assets"]["current_assets"]["financial_assets"]["trade_receivables"] = \
                                    p_values[0]

                        if re.search("Cash and cash equivalents", fs):
                            print("CASH : ", fs)
                            p_values = re.findall(two_numbers_pattern, fs)
                            if (len(p_values) > 1):
                                jsonData["to_year"]["assets"]["current_assets"]["financial_assets"][
                                    "cash_and_equivalents"] = p_values[0]
                                jsonData["from_year"]["assets"]["current_assets"]["financial_assets"][
                                    "cash_and_equivalents"] = p_values[1]
                            p_values = re.findall(left_dash_number_pattern, fs)
                            if len(p_values) == 1:

                                jsonData["from_year"]["assets"]["current_assets"]["financial_assets"][
                                    "cash_and_equivalents"] = p_values[1]

                            p_values = re.findall(right_dash_number_pattern, fs)
                            if len(p_values) == 1:
                                jsonData["to_year"]["assets"]["current_assets"]["financial_assets"][
                                    "cash_and_equivalents"] = p_values[0]

                        if re.search("Loans and advances", fs):
                            p_values = re.findall(two_numbers_pattern, fs)
                            if len(p_values) > 1:
                                jsonData["to_year"]["assets"]["current_assets"]["financial_assets"]["loans_and_advances"] = \
                                p_values[0]
                                jsonData["from_year"]["assets"]["current_assets"]["financial_assets"][
                                    "loans_and_advances"] = p_values[1]
                            p_values = re.findall(left_dash_number_pattern, fs)
                            if len(p_values) == 1:
                                jsonData["from_year"]["assets"]["current_assets"]["financial_assets"]["loans_and_advances"] = p_values[0]

                            p_values = re.findall(right_dash_number_pattern, fs)
                            if len(p_values) == 1:
                                jsonData["to_year"]["assets"]["current_assets"]["financial_assets"]["loans_and_advances"] = \
                                p_values[0]

                if re.search("Other current assets", crnt_asset_element):
                    p_values = re.findall(two_numbers_pattern, crnt_asset_element)
                    if len(p_values) > 1:
                        jsonData["to_year"]["assets"]["current_assets"]["other_current_assets"] = p_values[0]
                        jsonData["from_year"]["assets"]["current_assets"]["other_current_assets"] = p_values[1]
                    p_values = re.findall(left_dash_number_pattern, crnt_asset_element)
                    if len(p_values) == 1:
                        jsonData["from_year"]["assets"]["current_assets"]["other_current_assets"] = p_values[1]

                    p_values = re.findall(right_dash_number_pattern, crnt_asset_element)
                    if len(p_values) == 1:
                        jsonData["to_year"]["assets"]["current_assets"]["other_current_assets"] = p_values[0]
            #      EQUITIES AND LIABILITIES
            equities_liabilities_start_index = splittedText.index("EQUITIES AND LIABILITIES")
            eq_li_counter = equities_liabilities_start_index
            for eq_li in splittedText[equities_liabilities_start_index:]:
                if re.search("TOTAL EQUITY AND LIABILITIES", eq_li):
                    break
                if re.search("Equity",eq_li):
                    start_equity = eq_li_counter
                    for eq in splittedText[start_equity:]:
                        if re.search("Liabilities", eq):
                            break
                        if re.search("Share capital", eq):
                            p_values = re.findall(two_numbers_pattern, eq)
                            if len(p_values) > 1:
                                jsonData["to_year"]["equities_liabilities"]["equities"]["share_capital"] = p_values[0]
                                jsonData["from_year"]["equities_liabilities"]["equities"]["share_capital"] = p_values[1]
                            p_values = re.findall(left_dash_number_pattern, eq)
                            if len(p_values) == 1:
                                jsonData["from_year"]["equities_liabilities"]["equities"]["share_capital"] = p_values[1]

                            p_values = re.findall(right_dash_number_pattern, eq)
                            if len(p_values) == 1:
                                jsonData["to_year"]["equities_liabilities"]["equities"]["share_capital"] = p_values[0]

                        if re.search("Other equity", eq):
                            p_values = re.findall(two_numbers_pattern, eq)
                            if len(p_values) > 1:
                                jsonData["to_year"]["equities_liabilities"]["equities"]["other_capital"] = p_values[0]
                                jsonData["from_year"]["equities_liabilities"]["equities"]["other_capital"] = p_values[1]
                            p_values = re.findall(left_dash_number_pattern, eq)
                            if len(p_values) == 1:
                                jsonData["from_year"]["equities_liabilities"]["equities"]["other_capital"] = p_values[1]

                            p_values = re.findall(right_dash_number_pattern, eq)
                            if len(p_values) == 1:
                                jsonData["to_year"]["equities_liabilities"]["equities"]["other_capital"] = p_values[0]

            start_liabilities_index  = splittedText.index("Liabilities")
            lib_counter = start_liabilities_index
            for lib in splittedText[start_liabilities_index:]:
                if re.search("TOTAL EQUITY AND LIABILITIES", lib):
                    break

                if re.search("Non-current liabilities", lib):
                    non_current_start = lib_counter
                    non_current_counter = non_current_start
                    for non_current_lib in splittedText[non_current_start:]:
                        if re.search("Current liabilities", non_current_lib):
                            break
                        if re.search("Financial liabilities", non_current_lib):
                            for financial_lib in splittedText[non_current_counter:]:
                                if re.search("Provisions", financial_lib):
                                    break
                                if re.search("Borrowings", financial_lib):
                                    p_values = re.findall(two_numbers_pattern, financial_lib)
                                    if len(p_values) > 1:
                                        jsonData["to_year"]["equities_liabilities"]["liabilities"]["non_current_liabilities"]["financial_liabilities"]["borrowings"] = p_values[0]
                                        jsonData["from_year"]["equities_liabilities"]["liabilities"]["non_current_liabilities"]["financial_liabilities"]["borrowings"] = p_values[1]
                                    p_values = re.findall(left_dash_number_pattern, financial_lib)
                                    if len(p_values) == 1:
                                        jsonData["from_year"]["equities_liabilities"]["liabilities"]["non_current_liabilities"]["financial_liabilities"]["borrowings"] = p_values[1]

                                    p_values = re.findall(right_dash_number_pattern, financial_lib)
                                    if len(p_values) == 1:
                                        jsonData["to_year"]["equities_liabilities"]["liabilities"]["non_current_liabilities"]["financial_liabilities"]["borrowings"] = p_values[0]

                                if re.search("Lease Liabilities", financial_lib):
                                    p_values = re.findall(two_numbers_pattern, financial_lib)
                                    if len(p_values) > 1:
                                        jsonData["to_year"]["equities_liabilities"]["liabilities"]["non_current_liabilities"]["financial_liabilities"]["lease_liabilities"] = p_values[0]
                                        jsonData["from_year"]["equities_liabilities"]["liabilities"]["non_current_liabilities"]["financial_liabilities"]["lease_liabilities"] = p_values[1]
                                    p_values = re.findall(left_dash_number_pattern, financial_lib)
                                    if len(p_values) == 1:
                                        jsonData["from_year"]["equities_liabilities"]["liabilities"]["non_current_liabilities"]["financial_liabilities"]["lease_liabilities"] = p_values[1]

                                    p_values = re.findall(right_dash_number_pattern, financial_lib)
                                    if len(p_values) == 1:
                                        jsonData["to_year"]["equities_liabilities"]["liabilities"]["non_current_liabilities"]["financial_liabilities"]["lease_liabilities"] = p_values[0]

                        if re.search("Provisions", non_current_lib):
                            p_values = re.findall(two_numbers_pattern, financial_lib)
                            if len(p_values) > 1:
                                jsonData["to_year"]["equities_liabilities"]["liabilities"]["non_current_liabilities"]["provisions"] = p_values[0]
                                jsonData["from_year"]["equities_liabilities"]["liabilities"]["non_current_liabilities"]["provisions"] = p_values[1]
                            p_values = re.findall(left_dash_number_pattern, financial_lib)
                            if len(p_values) == 1:
                                jsonData["from_year"]["equities_liabilities"]["liabilities"]["non_current_liabilities"]["provisions"] = p_values[1]

                            p_values = re.findall(right_dash_number_pattern, financial_lib)
                            if len(p_values) == 1:
                                jsonData["to_year"]["equities_liabilities"]["liabilities"]["non_current_liabilities"]["provisions"] = p_values[0]

                        non_current_counter += 1

                if re.search("Current liabilities", lib):
                    current_start = lib_counter
                    current_counter = current_start
                    for current_lib in splittedText[current_start:]:
                        if re.search("TOTAL EQUITY AND LIABILITIES", current_lib):
                            break
                        print("Current : ", current_lib)
                        if re.search("Financial Liabilities", current_lib):
                            finance_start = current_counter
                            finance_counter  = finance_start
                            for financial_lib in splittedText[finance_start + 1:]:
                                if re.search("Provisions", financial_lib):
                                    break
                                if re.search("Borrowings", financial_lib):
                                    p_values = re.findall(two_numbers_pattern, financial_lib)
                                    if len(p_values) > 1:
                                        jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["borrowings"] = p_values[0]
                                        jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["borrowings"] = p_values[1]
                                    p_values = re.findall(left_dash_number_pattern, financial_lib)
                                    if len(p_values) == 1:
                                        jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["borrowings"] = p_values[1]
                                    p_values = re.findall(right_dash_number_pattern, financial_lib)
                                    if len(p_values) == 1:
                                        jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["borrowings"] = p_values[0]

                                if re.search("Lease Liabilities", financial_lib):
                                    p_values = re.findall(two_numbers_pattern, financial_lib)
                                    if len(p_values) > 1:
                                        jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["lease_liabilities"] = p_values[0]
                                        jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["lease_liabilities"] = p_values[1]
                                    p_values = re.findall(left_dash_number_pattern, financial_lib)
                                    if len(p_values) == 1:
                                        jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["lease_liabilities"] = p_values[1]

                                    p_values = re.findall(right_dash_number_pattern, financial_lib)
                                    if len(p_values) == 1:
                                        jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["lease_liabilities"] = p_values[0]
                                # Start Trade Payable
                                if re.search("Trade payables", financial_lib):
                                    trade_counter = finance_counter
                                    for trade_pay in splittedText[finance_counter + 1:]:
                                        trade_counter += 1
                                        if re.search("Others financial liabilities", trade_pay):
                                            break;
                                        if re.search("total outstanding dues of micro enterprises and small enterprises", trade_pay):
                                            p_values = re.findall(two_numbers_pattern, financial_lib)
                                            if len(p_values) > 1:
                                                jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["trade_payables"]["total_outstanding_dues_of_micro_enterprises_and_small_enterprises"]= p_values[0]
                                                jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["trade_payables"]["total_outstanding_dues_of_micro_enterprises_and_small_enterprises"] = p_values[1]
                                            p_values = re.findall(left_dash_number_pattern, financial_lib)
                                            if len(p_values) == 1:
                                                jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["trade_payables"]["total_outstanding_dues_of_micro_enterprises_and_small_enterprises"] = p_values[1]

                                            p_values = re.findall(right_dash_number_pattern, financial_lib)
                                            if len(p_values) == 1:
                                                jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["trade_payables"]["total_outstanding_dues_of_micro_enterprises_and_small_enterprises"] = p_values[0]
                                        if re.search("total outstanding dues of creditors other than micro enterprises and small", trade_pay):
                                            p_values = re.findall(two_numbers_pattern, financial_lib)
                                            found_count = 0
                                            if len(p_values) > 1:
                                                found_count += 1
                                                jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["trade_payables"]["total outstanding dues of creditors other than micro enterprises and small enterprises"]= p_values[0]
                                                jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["trade_payables"]["total outstanding dues of creditors other than micro enterprises and small enterprises"] = p_values[1]
                                            p_values = re.findall(left_dash_number_pattern, financial_lib)
                                            if len(p_values) == 1:
                                                found_count += 1
                                                jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["trade_payables"]["total outstanding dues of creditors other than micro enterprises and small enterprises"] = p_values[1]

                                            p_values = re.findall(right_dash_number_pattern, financial_lib)
                                            if len(p_values) == 1:
                                                found_count += 1
                                                jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["financial_liabilities"]["trade_payables"]["total outstanding dues of creditors other than micro enterprises and small enterprises"] = p_values[0]
                                            if found_count == 0:
                                                if re.search("enterprises", splittedText[trade_counter]):
                                                    print("HEHEHE : ", splittedText[trade_counter + 1])
                                                    p_values = re.findall(two_numbers_pattern, splittedText[trade_counter + 1])
                                                    found_count = 0
                                                    if len(p_values) > 1:
                                                        found_count += 1
                                                        jsonData["to_year"]["equities_liabilities"]["liabilities"][
                                                            "current_liabilities"]["financial_liabilities"][
                                                            "trade_payables"][
                                                            "total outstanding dues of creditors other than micro enterprises and small enterprises"] = \
                                                        p_values[0]
                                                        jsonData["from_year"]["equities_liabilities"]["liabilities"][
                                                            "current_liabilities"]["financial_liabilities"][
                                                            "trade_payables"][
                                                            "total outstanding dues of creditors other than micro enterprises and small enterprises"] = \
                                                        p_values[1]
                                                    p_values = re.findall(left_dash_number_pattern, splittedText[trade_counter + 1])
                                                    if len(p_values) == 1:
                                                        found_count += 1
                                                        jsonData["from_year"]["equities_liabilities"]["liabilities"][
                                                            "current_liabilities"]["financial_liabilities"][
                                                            "trade_payables"][
                                                            "total outstanding dues of creditors other than micro enterprises and small enterprises"] = \
                                                        p_values[1]

                                                    p_values = re.findall(right_dash_number_pattern, splittedText[trade_counter + 1])
                                                    if len(p_values) == 1:
                                                        found_count += 1
                                                        jsonData["to_year"]["equities_liabilities"]["liabilities"][
                                                            "current_liabilities"]["financial_liabilities"][
                                                            "trade_payables"][
                                                            "total outstanding dues of creditors other than micro enterprises and small enterprises"] = \
                                                        p_values[0]

                                if re.search("Others financial liabilities", financial_lib):
                                    p_values = re.findall(two_numbers_pattern, financial_lib)
                                    if len(p_values) > 1:
                                        jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"][
                                            "financial_liabilities"]["others_financial_liabilities"]= p_values[
                                            0]
                                        jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"][
                                            "financial_liabilities"]["others_financial_liabilities"] = p_values[
                                            1]
                                    p_values = re.findall(left_dash_number_pattern, financial_lib)
                                    if len(p_values) == 1:
                                        jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"][
                                            "financial_liabilities"]["others_financial_liabilities"] = p_values[
                                            1]

                                    p_values = re.findall(right_dash_number_pattern, financial_lib)
                                    if len(p_values) == 1:
                                        jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"][
                                            "financial_liabilities"]["others_financial_liabilities"] = p_values[
                                            0]

                                finance_counter += 1
                        if re.search("Provisions", current_lib):
                            p_values = re.findall(two_numbers_pattern, current_lib)
                            if len(p_values) > 1:
                                jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["provisions"] = p_values[
                                    0]
                                jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["provisions"] = p_values[
                                    1]
                            p_values = re.findall(left_dash_number_pattern, current_lib)
                            if len(p_values) == 1:
                                jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["provisions"] = p_values[
                                    1]

                            p_values = re.findall(right_dash_number_pattern, current_lib)
                            if len(p_values) == 1:
                                jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["provisions"] = p_values[
                                    0]

                        if re.search("Other current liabilities", current_lib):
                            p_values = re.findall(two_numbers_pattern, current_lib)
                            if len(p_values) > 1:
                                jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["other_current_liabilities"] = p_values[
                                    0]
                                jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["other_current_liabilities"] = p_values[
                                    1]
                            p_values = re.findall(left_dash_number_pattern, current_lib)
                            if len(p_values) == 1:
                                jsonData["from_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["other_current_liabilities"] = p_values[
                                    1]

                            p_values = re.findall(right_dash_number_pattern, current_lib)
                            if len(p_values) == 1:
                                jsonData["to_year"]["equities_liabilities"]["liabilities"]["current_liabilities"]["other_current_liabilities"] = p_values[
                                    0]
                lib_counter += 1
        i += 1

    if parser_count == 0:
        return []
    else:
        return jsonData
    