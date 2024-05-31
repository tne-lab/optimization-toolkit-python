const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    SendMsgToUITitle: (callback) => ipcRenderer.on('SendMsgToUI', (event, value) => callback(value)),
    setTitle: (val) => ipcRenderer.send('sendMessageToMainProcess', val)
});
