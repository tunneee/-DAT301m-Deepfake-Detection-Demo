import grpc
import tensorflow as tf

from keras.preprocessing import image
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

channel = grpc.insecure_channel('localhost:8500')
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

loaded_model = tf.saved_model.load("models/serving/1")
input_name = list(loaded_model.signatures['serving_default'].structured_input_signature[1].keys())[0]

def process_input_image(img_path):
    input_img = image.load_img(img_path, target_size= (64, 64))
    input_tensor = image.img_to_array(input_img)
    input_tensor = input_tensor.reshape(1, 64, 64, 3)
    input_tensor /= 255.
    return input_tensor

def grpc_infer(imgs):
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'deepfake-serving'
    result =request.inputs[input_name].CopyFrom(tf.make_tensor_proto(imgs, shape=imgs.shape))
    result = stub.Predict(request, 10.0)
    return result

def predict_image(img_path):
    input_tensor = process_input_image(img_path)
    result = grpc_infer(input_tensor)
    threshold = 0.7
    if result < threshold:
        return "Fake"
    else:
        return "Real"
    
    