# Pokémon MapReduce Analysis

## Description

This project analyzes a Pokémon dataset to determine the "feistiest" Pokémon for each type using the Hadoop MapReduce framework. Feistiness is defined as the ratio of attack points per kilogram of body weight (F = A/W). The job processes the dataset and outputs the Pokémon type along with the name of the Pokémon that has the highest feistiness within that type.

## Technologies Used

- **Hadoop (Version 3.4.1)** for distributed processing
- **Python** for writing the MapReduce scripts (mapper and reducer)
- **MapReduce** for parallel processing of the dataset
- **CSV format** for input and output

## Setup and Installation

### Prerequisites

- A single-node Hadoop cluster installed on Ubuntu (Version 3.4.1)
  - Set up a VirtualBox with **Ubuntu 24.04.1 LTS**.
  - Follow the official Hadoop documentation to install and configure Hadoop: [Hadoop Single-Node Setup](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html).
- **Java (OpenJDK 21.0)** installed.
  - Install Java using the following command:
    ```bash
    sudo apt install openjdk-21-jdk
    ```
- **Python 3.x** installed on the system.

### Steps

1. **Start Hadoop Services** Ensure Hadoop services are running:

   ```bash
   start-dfs.sh
   start-yarn.sh
   ```

2. **Download the Pokémon Dataset**

   - Download the dataset from [Kaggle](https://www.kaggle.com/datasets) and place it in the HDFS directory `/user/hadoop/`.
   - If the directory does not exist, create it:
     ```bash
     hadoop fs -mkdir -p /user/hadoop
     ```
   - Upload the dataset to HDFS:
     ```bash
     hadoop fs -put pokemon.csv /user/hadoop/pokemon.csv
     ```

3. **Upload Python Scripts**

   - Create a directory in HDFS (if needed):
     ```bash
     hdfs dfs -mkdir -p /user/hadoop/scripts
     ```
   - Upload the Python scripts to HDFS:
     ```bash
     hdfs dfs -put mapperA1.py /user/hadoop/scripts/
     hdfs dfs -put reducerA1.py /user/hadoop/scripts/
     ```
   - Verify the upload:
     ```bash
     hdfs dfs -ls /user/hadoop/scripts/
     ```
     If the scripts appear in the output, they have been successfully uploaded.

4. **Ensure the Correct File Paths**

   - Confirm that `pokemon.csv` exists in HDFS at `/user/hadoop/pokemon.csv`:
     ```bash
     hdfs dfs -ls /user/hadoop/
     ```

5. **Make Mapper and Reducer Executable**

   - Ensure both Python scripts have execution permissions:
     ```bash
     chmod +x mapperA1.py
     chmod +x reducerA1.py
     ```

6. **Run the MapReduce Job**

   - Since Hadoop Streaming does not execute Python scripts directly from HDFS, you need to ensure the scripts are available locally before running the job.
   - If your files are not in your local system, you can download them from HDFS by running:
     ```bash
     hdfs dfs -get /user/hadoop/scripts/mapperA1.py .
     hdfs dfs -get /user/hadoop/scripts/reducerA1.py .
     ```
   - Navigate to the directory where your files are stored locally.
   - Execute the following command to run the MapReduce job:
     ```bash
     hadoop jar /home/micaelasousai/Downloads/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar \
       -input /user/hadoop/pokemon.csv \
       -output /user/hadoop/output_new \
       -mapper mapperA1.py \
       -reducer reducerA1.py \
       -file mapperA1.py \
       -file reducerA1.py
     ```

      **Explanation:**

      - `-input /user/hadoop/pokemon.csv` : Specifies the dataset stored in HDFS.
      - `-output /user/hadoop/output_new` : Defines where the output will be saved in HDFS.
      - `-mapper mapperA1.py` : Assigns the mapper script.
      - `-reducer reducerA1.py` : Assigns the reducer script.
      - `-file mapperA1.py` and `-file reducerA1.py` : Ensures that these local scripts are copied to the worker nodes.

## Key Implementation Choices

### **Mapper**

- Extracts Pokémon types (type 1 and 2), name, attack points, and weight from the dataset.
- Calculates **feistiness** as `attack/weight`, rounded to two decimal places.
- Outputs key-value pairs where the Pokémon type1 is the key, and a comma-separated string of `type2, name, feistiness` is the value.

### **Reducer**

- Processes key-value pairs to identify the Pokémon with the highest feistiness for each type.
- Outputs a CSV file with the columns: **type1, type2, name, and feistiness**.

### **Handling Missing Values**

- **Missing Type 2 Values:** If a Pokémon does not have a `type2` value, it is replaced with an empty string (`""`). This ensures the dataset remains consistent and does not introduce additional placeholder values like `"NA"`.

- **Missing Weight Values:** Since weight (`weight_kg`) is necessary to calculate feistiness (`F = A/W`), any Pokémon with a missing weight is **skipped**. This prevents division by zero errors and ensures only meaningful feistiness scores are calculated.

- **Malformed or Incomplete Rows:**  
  - If a row has missing essential values (such as `attack` or `weight_kg`), it is skipped during processing.  
  - The mapper includes a `try-except` block to catch any errors from incorrect data formatting or missing fields, ensuring robustness.  
  - The reducer also checks for incorrect values and ignores them if they do not conform to the expected format.

### **Why Python?**

- Chosen for its simplicity and readability, making it easier to understand the MapReduce framework.

### **Why Hadoop Streaming?**

- Enables the use of Python scripts as mappers and reducers, aligning with the task requirements without needing Java-based MapReduce programs.

## Output Format

The output file contains the feistiest Pokémon for each type in CSV format:

```
type1,type2,name,feistiness 
bug,fairy,Cutiefly,225.0 
dark,flying,Murkrow,40.48 
...
```

To check if the output file was successfully stored, run:

```bash
hadoop fs -ls /user/hadoop/output_new
```

To check the contents of the output file, run:

```bash
hadoop fs -cat /user/hadoop/output_new/part-00000
```

To download the file to the local system, use the `get` command:

```bash
hadoop fs -get /user/hadoop/output_new/part-00000 /home/micaelasousai/Documents/pokemonOutput.csv
```

## Conclusion

This project demonstrates the power of Hadoop MapReduce for processing large datasets in parallel. By leveraging Python scripts and Hadoop Streaming, we efficiently compute the feistiest Pokémon for each type in a scalable and distributed manner.
