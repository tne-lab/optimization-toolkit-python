const path = require('path');
const { app, BrowserWindow, ipcMain } = require('electron');
const zmq = require('zeromq');

let mainWindow;
const reqSock = new zmq.Request();
const subSock = new zmq.Subscriber();

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            preload: path.join(__dirname, 'preload.js')
        }
    });

    mainWindow.loadFile('index.html');

    mainWindow.on('closed', () => {
        mainWindow = null;
    });

    connectToCSharpServer();
    connectToPubSubServer();
}

async function connectToCSharpServer() {
    const port = 'tcp://127.0.0.1:3090';
    try {
        await reqSock.connect(port);
        console.log('Connected to C# server');
        const data = {
            CommandType: "Initial Handshake",
            Data: {msg:'Hello from Electron!'}
        };
        await reqSock.send(JSON.stringify(data));
        const [result] = await reqSock.receive();
        console.log('Received data from C# server:', result.toString('utf-8'));
    } catch (error) {
        console.error('Error connecting to C# server:', error);
    }
}

async function connectToPubSubServer() {
    const port = 'tcp://127.0.0.1:3050';
    await subSock.connect(port);
    subSock.subscribe(''); // Subscribe to all topics
    console.log('Connected to Pub-Sub server');

    while (true) {
        try {
            const [message] = await subSock.receive();
            if (message !== undefined) {
                console.log('Received data from Management service:', message.toString('utf-8'));
                mainWindow.webContents.send('SendMsgToUI', "read this");
            } else {
                console.error('Received undefined message from Pub-Sub server');
            }
        } catch (error) {
            console.error('Error receiving message from Pub-Sub server:', error);
        }
    }
}

ipcMain.on('sendMessageToMainProcess', async (event, message) => {
    console.log('Sending message to C# server:', message);

    try {
        if (reqSock) {
            await reqSock.send(message);
            const [response] = await reqSock.receive();
            console.log('Received response from C# server:', response.toString('utf-8'));
            event.reply('responseFromCSharpServer', response.toString('utf-8'));
        } else {
            throw new Error('Connection to C# server is not established');
        }
    } catch (error) {
        console.error('Error sending/receiving message:', error);
    }
});

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
