<template>
  <div class="file-upload">
    <form @submit.prevent="onSubmit" enctype="multipart/form-data">
      <div class="upload-section">
        <h2>Please Upload Your File Here</h2> <!-- Capitalized text as requested -->
        <input type="file" id="file" ref="file" @change="onSelect" />
        <label for="file" class="custom-file-label">{{ file ? file.name : 'Choose file' }}</label>
        <button type="submit">Submit</button>
      </div>
      <div>
        <h5>{{ message }}</h5>
      </div>
      <div v-if="items.length" class="table-container">
        <v-data-table
          :headers="headers"
          :items="items"
          class="styled-table"
          :fixed-header="true"
          :height="'auto'"
        ></v-data-table>
      </div>
    </form>
  </div>
</template>



<script>
import axios from "axios";

export default {
  name: "FileUpload",
  data() {
    return {
      file: null,
      message: "",
      headers: [],
      items: [],
    };
  },
  methods: {
    onSelect() {
      const allowedTypes = ["text/csv"];
      const file = this.$refs.file.files[0];
      this.file = file;
      if (!allowedTypes.includes(file.type)) {
        this.message = "File type is not supported!";
        return;
      }
      if (file.size > 1024 * 1024 * 1024) { // Max file size 1GB
        this.message = "File too large, max size allowed is 1 GB";
        return;
      }
      this.message = ""; // Reset message on valid file selection
    },
    async onSubmit() {
      if (!this.file) {
        this.message = "Please select a file";
        return;
      }
      const formData = new FormData();
      formData.append("file", this.file);

      try {
        const response = await axios.post("http://localhost:8000/upload", formData);
        this.message = "Uploaded!";
        this.headers = Object.keys(response.data.data[0]).map(key => ({
          text: key.charAt(0).toUpperCase() + key.slice(1), // Capitalize headers
          value: key
        }));
        this.items = response.data.data;
      } catch (err) {
        this.message = err.response ? err.response.data.error : "Upload failed";
      }
    },
  },
};
</script>

<style scoped>
.file-upload {
  width: 100%;
  margin: 20px auto;
  font-family: Arial, sans-serif; /* You can change this to your preferred font */
}
form {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border-radius: 10px;
  background: #004c3f; /* Dark green background */
  color: white; /* White text */
}
.upload-section h2 {
  margin-bottom: 15px;
  text-align: center;
  font-size: 24px; /* Larger font size for visibility */
}
input[type="file"] {
  display: none; /* Hide the default input */
}
.custom-file-label {
  display: block;
  margin-bottom: 10px;
  padding: 10px 20px;
  background-color: white; /* White background */
  color: #00796b; /* Green text */
  font-size: 16px;
  text-align: center;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s ease;
  font-weight: bold; /* Make text bold */
}
.custom-file-label:hover {
  background-color: #e0f2f1; /* Light green background on hover */
}
button {
  padding: 10px 20px;
  background-color: white; /* White background */
  color: #00796b; /* Green text */
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s ease;
  font-weight: bold; /* Make text bold */
  margin: auto; /* Center button */
  display: block; /* Needed to allow margin auto to center */
}
button:hover {
  background-color: #e0f2f1; /* Light green background on hover */
}
.table-container {
  width: 100%;
  overflow-x: auto;
  margin-top: 20px;
}
.v-data-table {
  width: 100%;
  border-collapse: collapse;
}
::v-deep .v-data-table-header th {
  background-color: #00796b; /* Header green */
  color: white; /* White text */
  font-weight: bold;
  text-align: center;
}
::v-deep .v-data-table .v-data-table__wrapper table {
  text-align: center;
}
::v-deep .v-data-table tbody tr:nth-child(odd) {
  background-color: #ffffff; /* Odd rows white */
}
::v-deep .v-data-table tbody tr:nth-child(even) {
  background-color: #e0f2f1; /* Even rows light green */
}
</style>
