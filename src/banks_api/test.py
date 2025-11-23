import datetime

start = "2025-07-31"
end = "2026-01-30"

#
# start_obj = datetime.datetime.strptime(start, "%Y-%m-%d")
# end_obj = datetime.datetime.strptime(end, "%Y-%m-%d")
#
#
# month_selected = ((end_obj - start_obj).days // 30)
# print(month_selected)
#
#
# prev_date = ""
# next_date = ""
#
# date_containing = []
#
# if month_selected >= 3:
#     while month_selected > 0:
#
#         if prev_date == "":
#             prev_date = start
#
#         if next_date != "":
#             prev_date = next_date
#
#
#         if (datetime.datetime.strptime(prev_date, "%Y-%m-%d") + datetime.timedelta(days=90)) > datetime.datetime.now():
#             month_selected -= 3
#             continue
#
#         next_date = (datetime.datetime.strptime(prev_date, "%Y-%m-%d") + datetime.timedelta(days=90)).strftime("%Y-%m-%d")
#
#
#
#         date_containing.append({"start": prev_date, "end": next_date})
#
#         month_selected -= 3
# else:
#     date_containing.append({"start": start, "end": end})
#
#
# print(date_containing)