import pandas as pd 
from matplotlib import pyplot as plt

class When2Meet:
    # w2m_csv_path {str} - string path to the w2m csv data
    # names {list} - list of all members in the w2m
    # groups {dict} - {names: individuals in groups}
    def __init__(self, w2m_csv_path: str, names: list, groups: dict) -> None:
        self.df     = pd.read_csv(w2m_csv_path)
        self.names  = names
        self.groups = groups

    # Returns a filtered when2meet dataframe to only include members in a specific group of individuals
    # mem_query {list} - list of members to retain
    def __filter_group(self, mem_query: list) -> pd.DataFrame:
        _group_members = self.names.copy()
        for member in mem_query:
            _group_members.remove(member)

        return self.df.drop(columns=_group_members)

    # Returns a new pd.Series containing cummulative availability across individuals in time slots
    # filtered_w2m_df {pd.DataFrame} - w2m Dataframe that only contains desired names
    def __accumulate_availability(self, filtered_w2m_df: pd.DataFrame) -> pd.Series:
        cumm_availability = []
        for index, timeslot in filtered_w2m_df.drop(columns=["Day","Time"]).iterrows():
            cumm_val = 0
            for is_available in timeslot:
                if is_available:
                    cumm_val += 1
            cumm_availability.append(cumm_val)
        
        return pd.Series(data=cumm_availability, name="cumm")

    # Returns a table-friendly pd.Dataframe of the desired group of individuals in the w2m_dataframe
    # group_name {str} - name of group in self.groups to filter for
    def filter_table_distribution(self, group_name:str ) -> pd.DataFrame:
        df_filtered         = self.__filter_group(self.groups[group_name])
        df_filtered["cumm"] = self.__accumulate_availability(df_filtered)

        df_filtered         = df_filtered.drop(columns=self.groups[group_name])
        t_df = pd.DataFrame(data=df_filtered["Time"].drop_duplicates())
        
        for day in df_filtered["Day"].drop_duplicates():
            day_data = df_filtered[df_filtered["Day"] == f"{day}"]["cumm"].reset_index().drop(columns='index')
            t_df[f"{day}"] = day_data
        t_df = t_df.set_index("Time")

        return t_df
    
    def save_tablemap(self, filtered_table_df: pd.DataFrame, path: str) -> None:
        vals = filtered_table_df.values

        normal = plt.Normalize(vals.min()-1, vals.max()+1)
        fig = plt.figure(figsize=(15, 8))
        ax = fig.add_subplot(111, frameon=True, xticks=[], yticks=[])
        the_table = plt.table(
                        rowLabels=filtered_table_df.index,
                        colLabels=filtered_table_df.columns, 
                        loc='center', 
                        colWidths = [0.1]*vals.shape[1],
                        cellColours=plt.cm.YlGn(normal(vals))
                    )

        plt.savefig(path)