from IPython.core.magic import magics_class, Magics, line_magic, cell_magic, register_line_magic

from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

import get_trino_connection.get_trino_connection


@magics_class
class TrinoMagic(Magics):
    def __init__(self, shell):
        super().__init__(shell)
        self.conn = get_trino_connection()

    @cell_magic
    def trino(self, line, cell):
        params = {}
        df_name = None

        if line:
            parts = line.split("--")

            # Change: Apply strip() to the first element of the list (the DataFrame name)
            df_name = parts[0].strip() if parts else None

            if len(parts) > 1: # Check if parameters exist
                param_str = parts[1].strip() # Get the parameters string from the second element
                param_matches = re.findall(r"(\w+)\s*=\s*('[^']*'|\S+)", param_str)
                for key, value in param_matches:
                    value = value.strip("'") if value.startswith("'") and value.endswith("'") else value
                    params[key] = value

        try:
            cursor = self.conn.cursor()
            query = cell.format(**params)
            cursor.execute(query)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] # Access column names
            df = pd.DatafFrame(data, columns=columns)

            if df_name:
                self.shell.user_ns[df_name] = df
                print(f"DataFrame '{df_name}' created with {len(df)} rows."}
            else:
                print("No DataFrame name provided. Displaying results:")
                return df.head()

        except Exception as e:
            print(f"Execution failed: {e}")
        finally:
            if 'cursor' in locals() and cursor: # Check if cursor exists
                cursor.close()
            if 'self.conn' in locals() and self.conn: # Check if connection exists
                self.conn.close()

# Register the magic function
get_ipython().register_magics(TrinoMagic)

