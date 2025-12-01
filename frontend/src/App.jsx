import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Container, Typography, Box, TextField, Button, List, ListItem,
  ListItemText, IconButton, Select, MenuItem, CircularProgress, Chip
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

// --- API ---
// ЗМІНІТЬ НА ВАШУ URL (якщо вже задеплоїли) або залиште localhost
const api = axios.create({
  baseURL: 'https://task-man-project.onrender.com', 
});

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTitle, setNewTitle] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [loading, setLoading] = useState(true);

  // Завантаження завдань
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await api.get('/tasks/');
        setTasks(response.data);
      } catch (error) {
        console.error('Error loading tasks:', error);
      }
      setLoading(false);
    };
    fetchTasks();
  }, []);

  // Створення завдання
  const handleSubmit = async (event) => {
    event.preventDefault();
    const newTaskData = { title: newTitle, description: newDescription };
    try {
      const response = await api.post('/tasks/', newTaskData);
      setTasks([...tasks, response.data]);
      setNewTitle('');
      setNewDescription('');
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  // Оновлення статусу
  const handleUpdateStatus = async (id, newStatus) => {
    try {
      const response = await api.put(`/tasks/${id}`, { status: newStatus });
      setTasks(tasks.map((t) => (t.id === id ? response.data : t)));
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  // Видалення завдання
  const handleDelete = async (id) => {
    try {
      await api.delete(`/tasks/${id}`);
      setTasks(tasks.filter((t) => t.id !== id));
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  // Функція для форматування дати
  const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleString('uk-UA', {
      day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
    });
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Task Manager
        </Typography>

        <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4, p: 2, border: '1px solid #eee', borderRadius: 2 }}>
          <TextField
            fullWidth label="Назва задачі" variant="outlined"
            value={newTitle} onChange={(e) => setNewTitle(e.target.value)}
            required sx={{ mb: 2 }}
          />
          <TextField
            fullWidth label="Опис" variant="outlined"
            value={newDescription} onChange={(e) => setNewDescription(e.target.value)}
            sx={{ mb: 2 }}
          />
          <Button variant="contained" color="primary" type="submit">
            Додати задачу
          </Button>
        </Box>

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center' }}><CircularProgress /></Box>
        ) : (
          <List>
            {tasks.map((task) => (
              <ListItem
                key={task.id}
                secondaryAction={
                  <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(task.id)}>
                    <DeleteIcon color="error" />
                  </IconButton>
                }
                sx={{ 
                  border: '1px solid #ddd', mb: 2, borderRadius: '8px', 
                  bgcolor: '#fafafa', flexDirection: 'column', alignItems: 'flex-start' 
                }}
              >
                <Box sx={{ width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                  <Typography variant="h6">{task.title}</Typography>
                  <Select
                    value={task.status}
                    size="small"
                    onChange={(e) => handleUpdateStatus(task.id, e.target.value)}
                    sx={{ minWidth: 150 }}
                  >
                    {/* Використовуємо правильні значення з Enum */}
                    <MenuItem value="todo">📝 До виконання</MenuItem>
                    <MenuItem value="in_progress">⏳ В процесі</MenuItem>
                    <MenuItem value="done">✅ Готово</MenuItem>
                  </Select>
                </Box>
                
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {task.description || 'Без опису'}
                </Typography>

                <Box sx={{ width: '100%', display: 'flex', justifyContent: 'flex-end' }}>
                   <Chip label={`Створено: ${formatDate(task.created_at)}`} size="small" variant="outlined" />
                </Box>
              </ListItem>
            ))}
          </List>
        )}
      </Box>
    </Container>
  );
}

export default App;