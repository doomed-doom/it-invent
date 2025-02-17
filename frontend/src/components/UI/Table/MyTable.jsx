import React, { useMemo, useState, useEffect, useImperativeHandle, forwardRef } from 'react';
import { useTable, useSortBy } from 'react-table';
import { fetchData } from '../../../utils/fetchData';
import { Pencil } from 'lucide-react';
import classes from './MyTable.module.css';

const MyTable = forwardRef(({ columnlist, fulldata, onEditingChange }, ref) => {
    const currentTab = window.location.pathname.slice(1);
    const [data, setData] = useState(fulldata);
    const [editableCell, setEditableCell] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [newRowIndex, setNewRowIndex] = useState(null); // Индекс новой строки
    const [originalData, setOriginalData] = useState([]); // Храним исходные данные для восстановления
    const columns = useMemo(() => columnlist, [columnlist]);
    const [response, setResponse] = useState(null);
    const [fetchError, setFetchError] = useState(null);
    const [editedCells, setEditedCells] = useState({});

    // Константа, которая будет true, если редактируется любая ячейка с помощью Pencil
    const isEditingWithPencil = isEditing && editableCell !== null;

    useEffect(() => {
        if (onEditingChange) {
            onEditingChange(isEditingWithPencil);
        }
    }, [isEditingWithPencil, isEditing]);
    

    const tableInstance = useTable({ columns, data }, useSortBy);
    const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = tableInstance;

    const handleInputChange = (rowIndex, columnId, value) => {
        setEditedCells((prev) => ({
            ...prev,
            [`${rowIndex}-${columnId}`]: value,
        }));
        setData(prevData => {
            const newData = [...prevData];
            newData[rowIndex] = { ...newData[rowIndex], [columnId]: value };
            return newData;
        });
    };

    const handleEditClick = (rowIndex, columnId) => {
        setEditableCell({ rowIndex, columnId });
        setIsEditing(true);
    };
    
    
    const handleBlur = (event) => {
        setTimeout(() => {
            if (!document.activeElement.classList.contains(classes.input)) {
                setEditableCell(null);
                setIsEditing(false);
            }
        }, 100);
    };
    
    

    const addRow = () => {
        if (isEditing) return; // Если уже редактируем, не создаем новую строку
    
        // Проверяем, есть ли предыдущая строка и является ли она пустой
        const lastRowIndex = data.length - 1;
        const lastRow = data[lastRowIndex];
    
        const isLastRowEmpty = lastRow && Object.keys(lastRow).every((key) => {
            if (key === 'id') return true; // Пропускаем проверку для 'id'
            return lastRow[key] === "" || lastRow[key] === null || lastRow[key] === undefined;
        });
    
        if (isLastRowEmpty) {
            // Если предыдущая строка пустая, делаем её редактируемой
            setEditableCell({ rowIndex: lastRowIndex, columnId: columnlist[0].accessor });
            setIsEditing(true);
            onEditingChange?.(true); // Сообщаем родительскому компоненту о начале редактирования
        } else {
            // Если предыдущая строка не пустая, добавляем новую строку
            setData(prevData => {
                const newRow = { id: prevData.length ? prevData[prevData.length - 1].id + 1 : 1 };
                columnlist.forEach(col => newRow[col.accessor] = col.accessor === 'id' ? newRow.id : "");
    
                setNewRowIndex(prevData.length);
                setEditableCell({ rowIndex: prevData.length, columnId: columnlist[0].accessor });
                setIsEditing(true);
                onEditingChange?.(true); // Сообщаем родительскому компоненту о начале редактирования
    
                return [...prevData, newRow];
            });
        }
    };
    
    
    const cancelEdit = () => {
        setData(prevData => {
            if (newRowIndex !== null) {
                return prevData.filter((row, index) => index !== newRowIndex);
            }
            return originalData.length ? originalData : prevData;
        });
        setEditableCell(null);
        setIsEditing(false);
        setNewRowIndex(null);
        setEditedCells({});
        setOriginalData([]);
        onEditingChange?.(false); // Явно передаем, что редактирование отменено
    };
    

    const sendData = async () => {
        if (Object.keys(editedCells).length > 0) {
            const updatedRows = {};
            const rowsToDelete = []; // Массив для хранения индексов строк, которые нужно удалить
    
            // Сначала собираем все изменённые строки
            Object.keys(editedCells).forEach((key) => {
                const [rowIndex, columnId] = key.split('-');
                if (columnId !== 'id') {
                    if (!updatedRows[rowIndex]) {
                        updatedRows[rowIndex] = { ...data[rowIndex] };
                    }
                    updatedRows[rowIndex][columnId] = editedCells[key];
                }
            });
    
            // Проверяем, есть ли пустые строки среди изменённых
            Object.keys(updatedRows).forEach((rowIndex) => {
                const row = updatedRows[rowIndex];
                const isEmptyRow = Object.keys(row).every((key) => {
                    if (key === 'id') return true; // Пропускаем проверку для 'id'
                    return row[key] === "" || row[key] === null || row[key] === undefined;
                });
    
                if (isEmptyRow) {
                    rowsToDelete.push(rowIndex); // Добавляем индекс строки для удаления
                }
            });
    
            // Удаляем пустые строки из данных
            const updatedData = data.filter((row, index) => !rowsToDelete.includes(index.toString()));
    
            // Отправляем оставшиеся данные на сервер
            for (const updatedRow of Object.values(updatedRows)) {
                try {
                    if (rowsToDelete.includes(updatedRow.id.toString())) {
                        continue; // Пропускаем удалённые строки
                    }
    
                    if (updatedRow.id > Math.max(...data.map(row => row.id), 0)) {
                        console.log("Создание новой строки:", updatedRow);
                        const response = await fetchData(`${currentTab}`, 'post', updatedRow);
                        if (response) {
                            updatedData.push(response);
                        }
                    } else {
                        console.log(`Обновление данных для id ${updatedRow.id}:`, updatedRow);
                        const response = await fetchData(`${currentTab}/${updatedRow.id}`, 'put', updatedRow);
                        if (response) {
                            const index = updatedData.findIndex(row => row.id === updatedRow.id);
                            if (index !== -1) {
                                updatedData[index] = { ...updatedData[index], ...updatedRow };
                            }
                        }
                    }
                } catch (error) {
                    console.error("Ошибка при отправке данных:", error);
                }
            }
    
            // Обновляем состояние
            setData(updatedData);
            setOriginalData([...updatedData]); // Обновляем originalData после успешного сохранения
            setEditedCells({});
            setIsEditing(false);
            setNewRowIndex(null);
        }
    };
    
    
    useImperativeHandle(ref, () => ({
        addRow,
        cancelEdit,
        sendData,
        isEditing
    }));
    
    
    useEffect(() => {
        setData(fulldata);
    }, [fulldata]);

    return (
        <div className={classes.container}>
            <table className={classes.table} {...getTableProps()}>
                <thead>
                    {headerGroups.map((headerGroup, index) => (
                        <tr {...headerGroup.getHeaderGroupProps()} key={index} className={classes.table__row}>
                            {headerGroup.headers.map((column) => (
                                <th {...column.getHeaderProps()} key={column.id} className={classes.table__cell}>
                                    {column.render('Header')}
                                </th>
                            ))}
                        </tr>
                    ))}
                </thead>
                <tbody {...getTableBodyProps()}>
                    {rows.map((row, rowIndex) => {
                        prepareRow(row);
                        const isNewRow = rowIndex === newRowIndex; // Проверяем, является ли строка новой
                        return (
                            <tr {...row.getRowProps()} key={rowIndex} className={classes.table__row}>
                                {row.cells.map((cell) => (
                                    <td {...cell.getCellProps()} key={cell.column.id} className={classes.table__cell}>
                                        {cell.column.id === 'id' ? ( // Если столбец 'id', то ячейка нередактируемая
                                            <div className={classes.cellContent}>
                                                {cell.render('Cell')}
                                            </div>
                                        ) : (editableCell?.rowIndex === rowIndex && editableCell?.columnId === cell.column.id) ? (
                                            // Редактируемая ячейка (одиночная)
                                            <input
                                                className={classes.input}
                                                value={editedCells[`${rowIndex}-${cell.column.id}`] || data[rowIndex][cell.column.id] || ''}
                                                onChange={(e) => handleInputChange(rowIndex, cell.column.id, e.target.value)}
                                                onBlur={handleBlur}
                                                autoFocus
                                            />
                                        ) : isNewRow && cell.column.id !== 'id' ? (
                                            // Новая строка (все ячейки, кроме 'id', редактируемые)
                                            <input
                                                className={classes.input}
                                                value={editedCells[`${rowIndex}-${cell.column.id}`] || data[rowIndex][cell.column.id] || ''}
                                                onChange={(e) => handleInputChange(rowIndex, cell.column.id, e.target.value)}
                                                onBlur={handleBlur}
                                            />
                                        ) : (
                                            // Обычная ячейка (нередактируемая)
                                            <div className={classes.cellContent}>
                                                {editedCells[`${rowIndex}-${cell.column.id}`] || cell.render('Cell')}
                                                {(cell.column.id === 'Статус' || cell.column.id.startsWith('Сотрудник') || cell.column.id === 'Адрес') && (
                                                    <Pencil
                                                        className={classes.editIcon}
                                                        size={16}
                                                        onClick={() => handleEditClick(rowIndex, cell.column.id)}
                                                    />
                                                )}
                                            </div>
                                        )}
                                    </td>                                                                
                                ))}
                            </tr>
                        );
                    })}
                </tbody>
            </table>
            {fetchError && <div>{fetchError}</div>}
        </div>
    );
});

export { MyTable };