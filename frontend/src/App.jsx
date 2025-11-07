import React, { useState, useEffect } from 'react';
import axios from 'axios'; // <-- Импортируем 'телефон'

// --- ИМПОРТЫ КОМПОНЕНТОВ MUI ---
import {
  Container,
  Typography,
  Box,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Select,
  MenuItem,
  CircularProgress, // <-- Добавили индикатор загрузки
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

// --- 1. Настраиваем наш "телефон" (API-клиент) ---
// Он будет автоматически "звонить" на ваш бэкенд
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

function App() {
  // --- 2. "Память" (State) ---
  const [tasks, setTasks] = useState([]); // <-- Начинаем с ПУСТОГО списка
  const [newTitle, setNewTitle] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [loading, setLoading] = useState(true); // <-- Состояние для загрузки

  // --- 3. "Загрузчик данных" (Effect) ---
  // Этот код выполняется ОДИН РАЗ при загрузке страницы
  useEffect(() => {
    // Создаем функцию, чтобы загрузить задачи
    const fetchTasks = async () => {
      try {
        const response = await api.get('/tasks/');
        setTasks(response.data); // <-- Кладём настоящие задачи в "память"
      } catch (error) {
        console.error('Ошибка при загрузке задач:', error);
      }
      setLoading(false); // <-- Убираем индикатор загрузки
    };

    fetchTasks(); // <-- Вызываем функцию
  }, []); // <-- Пустой массив [] означает "выполнить один раз"

  // --- 4. "Обработчик отправки" (Event Handler) ---
  const handleSubmit = async (event) => {
    event.preventDefault(); // <-- НЕ перезагружать страницу!

    // 1. Готовим данные для отправки
    const newTaskData = {
      title: newTitle,
      description: newDescription,
    };

    try {
      // 2. Отправляем данные на бэкенд
      const response = await api.post('/tasks/', newTaskData);

      // 3. Обновляем список на лету, не перезагружая страницу
      // response.data - это задача, которую вернул нам FastAPI
      setTasks([...tasks, response.data]);

      // 4. Очищаем поля ввода
      setNewTitle('');
      setNewDescription('');
    } catch (error) {
      console.error('Ошибка при создании задачи:', error);
    }
  };

  // --- "Оживляем" ОБНОВЛЕНИЕ СТАТУСА ---
  const handleUpdateStatus = async (id, newStatus) => {
    try {
      // 1. Готовим данные для отправки (только статус)
      const updateData = { status: newStatus };
      
      // 2. Отправляем PUT-запрос на бэкенд
      const response = await api.put(`/tasks/${id}`, updateData);

      // 3. Обновляем "память" (State), чтобы React перерисовал
      //    список с новым статусом
      setTasks(
        tasks.map((task) =>
          task.id === id ? response.data : task
        )
      );
    } catch (error) {
      console.error('Ошибка при обновлении статуса:', error);
    }
  };

  // --- "Оживляем" УДАЛЕНИЕ ---
  const handleDelete = async (id) => {
    try {
      // 1. Отправляем запрос на бэкенд
      await api.delete(`/tasks/${id}`);
      
      // 2. Обновляем "память" (State), удаляя эту задачу из списка
      //    Это заставит React перерисовать интерфейс
      setTasks(tasks.filter((task) => task.id !== id));
      
    } catch (error) {
      console.error('Ошибка при удалении задачи:', error);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Task Manager
        </Typography>

        {/* --- Форма "ожила": добавили onSubmit, value и onChange --- */}
        <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
          <TextField
            fullWidth
            label="Название задачи"
            variant="outlined"
            value={newTitle} // <-- Привязка к "памяти"
            onChange={(e) => setNewTitle(e.target.value)} // <-- Обновление "памяти"
            required // <-- Поле стало обязательным
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Описание"
            variant="outlined"
            value={newDescription} // <-- Привязка к "памяти"
            onChange={(e) => setNewDescription(e.target.value)} // <-- Обновление "памяти"
            sx={{ mb: 2 }}
          />
          <Button variant="contained" color="primary" type="submit">
            Добавить задачу
          </Button>
        </Box>

        {/* --- Список задач (теперь "живой") --- */}
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center' }}>
            <CircularProgress /> {/* Показываем "крутилку" во время загрузки */}
          </Box>
        ) : (
          <List>
            {tasks.map((task) => (
              <ListItem
                key={task.id}
                secondaryAction={
                  <IconButton
                    edge="end"
                    aria-label="delete"
                    onClick={() => handleDelete(task.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                }
                sx={{ border: '1px solid #ddd', mb: 1, borderRadius: '4px' }}
              >
                <ListItemText
                  primary={task.title}
                  secondary={task.description || 'Нет описания'}
                />
                <Select
                  value={task.status}
                  size="small"
                  onChange={(e) => handleUpdateStatus(task.id, e.target.value)}
                  sx={{ ml: 2, minWidth: 120 }}
                >
                  <MenuItem value="todo">К выполнению</MenuItem>
                  <MenuItem value="in_progress">В процессе</MenuItem>
                  <MenuItem value="done">Готово</MenuItem>
                </Select>
              </ListItem>
            ))}
          </List>
        )}
      </Box>
    </Container>
  );
}

export default App;

