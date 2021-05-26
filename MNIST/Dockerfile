FROM tensorflow/tensorflow:latest-gpu

RUN pip3 install py3nvml pynvml flask
ADD ./model /model
ADD main.py /main.py

EXPOSE 8051

ENTRYPOINT ["python3", "/main.py", "&"]
