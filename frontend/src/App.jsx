import React from "react";
import Inbox from "./pages/Inbox";
import { AppBar, Toolbar, Typography, Container, CssBaseline, Box } from "@mui/material";

function App() {
  return (
    <>
      <CssBaseline /> {/* Estilos base de MUI */}
      <AppBar position="static" color="primary" elevation={3}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, textAlign: "center" }}>
            Clasificador de Correos
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Box>
          <Inbox />
        </Box>
      </Container>
    </>
  );
}

export default App;
