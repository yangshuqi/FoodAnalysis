function get_image(listen, filename)

while listen.BytesAvailable == 0
    pause(1)
    disp('wait')
end

data0 = fread(listen, listen.BytesAvailable);

fid = fopen(filename,'wb');  
SIZE = str2num(char(data0'))
buf_size = 1024;
now_size = 0;
flag = 0;
while now_size < SIZE
    pause(0.1)
    data = fread(listen, min(SIZE-now_size, buf_size));
    fwrite(fid, data);
    disp(flag); flag = flag + 1;
    now_size = now_size + buf_size;
end

fclose(fid);

end