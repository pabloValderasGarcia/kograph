// import { notify } from 'notiwind';
import axios from "axios";

export async function uploadFile(file) {
    const token = localStorage.getItem('access');

    const formData = new FormData();
    formData.append('user', token);
    formData.append('file', file.file, file.file.name);
    formData.append('title', file.file.name);

    try {
        const response = await axios.post(`${process.env.VUE_APP_SERVER_URL}/file/upload/`, formData, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'multipart/form-data',
            },
        });
        return { 'status': true, 'response': response };
    } catch (error) {
        return { 'status': false, 'error': error };
    }
}

export default function createUploader() {
    return {
        uploadFile: function (file) {
            return uploadFile(file)
        }
    }
}