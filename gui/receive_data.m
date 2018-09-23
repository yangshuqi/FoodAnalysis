function[images, infos] = receive_data(ip, port)

listen = tcpip(ip,port,'NetworkRole','server');

buf_size = 1024;
listen.InputBufferSize = buf_size;
listen.Timeout = 10;

fopen(listen);
disp('fopen');

while listen.BytesAvailable == 0
    pause(1)
    disp('wait')
end

data0 = fread(listen, listen.BytesAvailable);
data0 = char(data0');
data0 = strsplit(data0, ';');
img_idx = 1;
info_idx = 1;
images = {};
infos = {};
for k = 1: length(data0)-1
    type = data0{k}
    if strcmp(type, 'image')
        get_image(listen, [int2str(k), '.jpg'])
        images{img_idx} = [int2str(k), '.jpg'];
        img_idx = img_idx + 1;
    end
    if strcmp(type, 'info') 
        while listen.BytesAvailable == 0
        end
        in = fread(listen, listen.BytesAvailable);
        in = char(in')
        infos{info_idx} = in;
        info_idx = info_idx + 1;
    end
end
fclose(listen);
fprintf('接收成功并且已经写入文件\n');
