//Terminal: yarn start

import React, { useState } from "react";
import { Button, Container, Typography, TextField } from "@mui/material";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null); // Datei
  const [message, setMessage] = useState(""); // Statusnachricht

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const uploadFile = async () => {
    if (!file) {
      setMessage("Bitte wählen Sie eine Datei aus.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/transform-csv/",
        formData,
        {
          responseType: "blob", // Um die Datei herunterzuladen
        }
      );

      // Datei herunterladen
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "transformed_coordinates.csv");
      document.body.appendChild(link);
      link.click();
      link.remove();

      setMessage("Datei erfolgreich transformiert und heruntergeladen.");
    } catch (error) {
      console.error("Fehler bei der Anfrage:", error);
      setMessage("Fehler bei der Transformation der Datei.");
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        CSV Koordinatentransformation (WGS84 zu LV95)
      </Typography>

      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        style={{ marginBottom: "20px", display: "block" }}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={uploadFile}
        style={{ marginBottom: "20px" }}
      >
        Datei hochladen und transformieren
      </Button>

      {message && (
        <Typography
          variant="body1"
          style={{ marginTop: "20px", color: "green" }}
        >
          {message}
        </Typography>
      )}
    </Container>
  );
}

export default App;
