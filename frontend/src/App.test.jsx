import { vi, test, expect, beforeEach } from 'vitest';
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react'; 
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import App from './App';
import axios from 'axios'; 

const { mockedApi } = vi.hoisted(() => {
  return {
    mockedApi: {
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
    }
  };
});

vi.mock('axios', () => ({
  default: {
    create: () => mockedApi,
  },
}));
// -----------------------------------------------------


// --- 2. Подготовка данных для моков ---
const mockTasks = [
  { id: 1, title: 'Задача 1', description: 'Описание 1', status: 'todo' },
  { id: 2, title: 'Задача 2', description: 'Описание 2', status: 'in_progress' },
];

// --- 3. Очистка моков перед каждым тестом ---
beforeEach(() => {
  mockedApi.get.mockClear();
  mockedApi.post.mockClear();
  mockedApi.put.mockClear();
  mockedApi.delete.mockClear();
});



test('1. Отображает загрузчик и загружает задачи', async () => {
  // Arrange (Подготовка)
  mockedApi.get.mockResolvedValue({ data: mockTasks });

  // Act (Действие)
  render(<App />);

  // Assert (Проверка)
  expect(screen.getByRole('progressbar')).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
  });

  expect(screen.getByText('Задача 1')).toBeInTheDocument();
  expect(screen.getByText('Описание 2')).toBeInTheDocument();
  expect(mockedApi.get).toHaveBeenCalledWith('/tasks/');
});

test('2. Позволяет создать новую задачу', async () => {
  // Arrange
  const newTask = { 
    id: 3, 
    title: 'Новая задача', 
    description: 'Новое описание', 
    status: 'todo' 
  };
  
  mockedApi.get.mockResolvedValue({ data: [] });
  mockedApi.post.mockResolvedValue({ data: newTask });

  render(<App />);
  await waitFor(() => {
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
  });

  // Act
    await userEvent.type(screen.getByLabelText(/Название задачи/i), newTask.title);
  
  await userEvent.type(screen.getByLabelText('Описание'), newTask.description);

  await userEvent.click(screen.getByRole('button', { name: 'Добавить задачу' }));

  // Assert
  expect(await screen.findByText('Новая задача')).toBeInTheDocument();
  expect(mockedApi.post).toHaveBeenCalledWith('/tasks/', {
    title: newTask.title,
    description: newTask.description,
  });
  
  // Ищем поле по-новому, чтобы проверить, что оно очистилось
  expect(screen.getByLabelText(/Название задачи/i)).toHaveValue('');
});

test('3. Позволяет удалить задачу', async () => {
  // Arrange
  mockedApi.get.mockResolvedValue({ data: [mockTasks[0]] });
  mockedApi.delete.mockResolvedValue({ status: 204 });

  render(<App />);
  expect(await screen.findByText('Задача 1')).toBeInTheDocument();

  // Act
  await userEvent.click(screen.getByLabelText('delete'));

  // Assert
  await waitFor(() => {
    expect(screen.queryByText('Задача 1')).not.toBeInTheDocument();
  });
  expect(mockedApi.delete).toHaveBeenCalledWith(`/tasks/${mockTasks[0].id}`);
});

test('4. Позволяет обновить статус задачи', async () => {
  // Arrange
  const updatedTask = { ...mockTasks[0], status: 'done' };
  mockedApi.get.mockResolvedValue({ data: [mockTasks[0]] });
  mockedApi.put.mockResolvedValue({ data: updatedTask });

  render(<App />);
  await screen.findByText('Задача 1');
  
  const statusSelect = screen.getByRole('combobox');
  expect(statusSelect).toHaveTextContent('К выполнению');

  // Act
  await userEvent.click(statusSelect);
  await userEvent.click(screen.getByRole('option', { name: 'Готово' }));

  // Assert
  await waitFor(() => {
    expect(mockedApi.put).toHaveBeenCalledWith(
      `/tasks/${mockTasks[0].id}`, 
      { status: 'done' }
    );
  });
  expect(statusSelect).toHaveTextContent('Готово');
});