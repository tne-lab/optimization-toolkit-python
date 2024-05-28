// main.js

const path = require('path');
const { app, BrowserWindow, ipcMain } = require('electron');
const net = require('net');
const { channel } = require('diagnostics_channel');
const { listeners } = require('process');

let mainWindow;
let clientSocket;

function createWindow() {
    console.log('Creating window...');
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            preload: path.join(process.cwd(), 'preload.js')
        }
    });

    mainWindow.loadFile('index.html');

    mainWindow.on('closed', () => {
        console.log('Window closed.');
        mainWindow = null;
    });

    connectToWindowsService();
}

function connectToWindowsService() {
    console.log('Connecting to Windows service...');
    const port = 3000; // Port number where Windows service is running
    const hostname = '127.0.0.1'; // IP address of the Windows machine

    clientSocket = new net.Socket();

    clientSocket.connect(port, hostname, () => {
        console.log('Connected to Windows service');

        // Once connected, send some text to the Windows service
        const message = 'Hello from Electron!';
        clientSocket.write(message);
    });

    clientSocket.on('data', (data) => {
        console.log('Received data from Windows service:', data.toString('utf-8'));
        // You can further process the received data or update the UI as needed
    });

    clientSocket.on('error', (err) => {
        console.error('Error connecting to Windows service:', err.message);
    });

    clientSocket.on('close', () => {
        console.log('Connection to Windows service closed');
    });
}


// Handle IPC message from renderer process to send message to Windows service
ipcMain.on('sendMessageToMainProcess', (event, message) => {

    console.log('Received message from renderer process:');

    if (clientSocket && clientSocket.writable) {
        console.log('Sending message to Windows service...');
        clientSocket.write(message);
    } else {
        console.error('Cannot send message: Connection to Windows service is not established');
    }
});

app.on('ready', () => {
    console.log('App ready.');
    createWindow();
});

app.on('window-all-closed', () => {
    console.log('All windows closed.');
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
