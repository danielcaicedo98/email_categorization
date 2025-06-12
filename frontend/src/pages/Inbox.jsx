import { useEffect, useState } from "react";
import {
  Box,
  Tabs,
  Tab,
  Typography,
  List,
  ListItemButton,
  ListItemText,
  Collapse,
  Paper,
  CircularProgress,
  Card,
  CardContent,
  Divider,
} from "@mui/material";
import { ExpandLess, ExpandMore } from "@mui/icons-material";

const categorias = [
  "Todos",
  "Profesional",
  "Personal",
  "Finanzas",
  "Citas",
  "Spam",
  "Facturas",
  "General",
  "Académico",
];

export default function Inbox() {
  const [correos, setCorreos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState("Todos");
  const [correoAbierto, setCorreoAbierto] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/correos")
      .then((res) => res.json())
      .then((data) => {
        setCorreos(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error al obtener correos:", err);
        setLoading(false);
      });
  }, []);

  const handleTabChange = (event, newValue) => {
    setCategoriaSeleccionada(newValue);
    setCorreoAbierto(null);
  };

  const correosFiltrados = correos.filter((correo) =>
    categoriaSeleccionada === "Todos"
      ? true
      : correo.categoria === categoriaSeleccionada
  );

  const toggleCorreo = (index) => {
    setCorreoAbierto(correoAbierto === index ? null : index);
  };

  if (loading) {
    return (
      <Box
        sx={{
          height: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
        }}
      >
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Cargando correos...
        </Typography>
      </Box>
    );
  }

  return (
    <Card elevation={4} sx={{ p: 2 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Bandeja de Entrada
        </Typography>

        <Tabs
          value={categoriaSeleccionada}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          aria-label="Categorías"
          sx={{ mb: 2 }}
        >
          {categorias.map((cat) => (
            <Tab key={cat} label={cat} value={cat} />
          ))}
        </Tabs>

        <Divider sx={{ mb: 2 }} />

        <List component="nav" disablePadding>
          {correosFiltrados.map((correo, index) => (
            <Box key={index}>
              <ListItemButton onClick={() => toggleCorreo(index)}>
                <ListItemText
                  primary={
                    <Typography variant="subtitle1" fontWeight="bold">
                      {correo.asunto}
                    </Typography>
                  }
                  secondary={
                    <Typography variant="body2" color="text.secondary">
                      {correo.cuerpo.slice(0, 120)}...
                    </Typography>
                  }
                />
                {correoAbierto === index ? <ExpandLess /> : <ExpandMore />}
              </ListItemButton>

              <Collapse in={correoAbierto === index} timeout="auto" unmountOnExit>
                <Box sx={{ px: 3, py: 2, bgcolor: "#f9f9f9" }}>
                  <Typography variant="body1" sx={{ whiteSpace: "pre-line" }}>
                    {correo.cuerpo}
                  </Typography>
                </Box>
              </Collapse>

              <Divider />
            </Box>
          ))}
        </List>
      </CardContent>
    </Card>
  );
}
