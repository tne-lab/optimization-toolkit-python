// main.js -- using zeromq for the communication

const path = require('path');
const { app, BrowserWindow, ipcMain } = require('electron');
const net = require('net');
const { channel } = require('diagnostics_channel');
const { listeners } = require('process');
const zmq = require('zeromq');
const sock = new zmq.Request();
const sock1 = new zmq.Request();
const sock2 = new zmq.Request();
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
    console.log('Connecting to Windows service...', zmq.version);
    const port = 'tcp://127.0.0.1:3000'; // Port number where DRA service is running
    const port1 = 'tcp://127.0.0.1:3002'; // Port number where DRA service is running
    const port2 = 'tcp://127.0.0.1:3057'; // Port number where DRA service is running
    sock.connect(port);
    sock1.connect(port1);
    sock2.connect(port2);
    console.log('Connected to Windows service');
    var data = {
        DataType: "InitiationData",
        MessageSend: 'Hello from Electron!'
    };
    await sock.send(JSON.stringify(data));
    const [result] = await sock.receive();

    console.log('Received data from Windows service:', result.toString('utf-8'));

    // sock.close();
    // console.log('Connection to Windows service closed');
}




// Handle IPC message from renderer process to send message to Windows service
ipcMain.on('sendMessageToMainProcess', async (event, message) => {
    console.log('Received message from renderer process:');

    if (sock && sock1) {
        console.log('Sending message to Windows service python...');
        await sock1.send(message);
        const [result1] = await sock1.receive();
        console.log('Received data from Windows service on port 3002:', result1.toString('utf-8'));
        console.log('Sending received data to Windows service on port 3000...');
        console.log(result1.toString('utf-8'),"---------------------",message);
        console.log('Sending message to Windows service database...');
        await sock.send(result1.toString('utf-8'));
        const [result] = await sock.receive();
        console.log('Received data from Windows service database:', result.toString('utf-8'));
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
