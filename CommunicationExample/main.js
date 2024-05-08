// main.js -- using zeromq for the communication

const path = require('path');
const { app, BrowserWindow, ipcMain } = require('electron');
const net = require('net');
const { channel } = require('diagnostics_channel');
const { listeners } = require('process');
const zmq = require('zeromq');
const sock = new zmq.Request();

let mainWindow;
//let clientSocket;

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


async function connectToWindowsService() {
    console.log('Connecting to Windows service...');
    const port = 'tcp://127.0.0.1:3000'; // Port number where Windows service is running

    sock.connect(port);
    console.log('Connected to Windows service');

    await sock.send('Hello from Electron!');
    const [result] = await sock.receive();

    console.log('Received data from Windows service:', result.toString('utf-8'));

    // sock.close();
    // console.log('Connection to Windows service closed');
}




// Handle IPC message from renderer process to send message to Windows service
ipcMain.on('sendMessageToMainProcess', async (event, message) => {
  console.log('Received message from renderer process:');

  if (sock) {
      console.log('Sending message to Windows service...');
      await sock.send(message);
      const [result] = await sock.receive();
      console.log('Received data from Windows service:', result.toString('utf-8'));
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
