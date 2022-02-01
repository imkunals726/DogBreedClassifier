from django.http                import HttpResponseRedirect, HttpResponse
from django.shortcuts           import render
from rest_framework.decorators  import api_view
from .forms                     import ImageForm
from .constants                 import class_names

import numpy as np , tensorflow as tf, cv2, base64
dognet  = tf.keras.models.load_model('dognet/dognet')

@api_view(['POST', 'GET'])
def get_image(request):
    # if this is a POST request we need to process the form data
    print(request.method, 'method')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImageForm(request.POST, request.FILES)

        

        if form.is_valid():
            print(form)

            img     = cv2.imdecode(np.fromstring(request.FILES['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)

            cv2.imwrite('static/color_img.jpg', img)

            img1 = cv2.imread('static/color_img.jpg')
            
            ret, frame_buff = cv2.imencode('.jpg', img1)
            frame_b64 = base64.b64encode(frame_buff)

            test_set = [cv2.resize(img,(256, 256))]
            test_set = np.array(test_set, np.float32)/255.0

            predictions= dognet.predict(test_set)

            preds = np.argsort(predictions, axis=1)

            cn = [class_names[idx] for idx in preds[0][-5:]]
            pr = [predictions[0][idx] for idx in preds[0][-5:]]

            xValues = cn
            yValues = pr

        print(xValues)
        print(yValues)
      


        return render(request, 'index.html', {'xValues' : xValues , 'yValues' : yValues ,  'form' : form , 'img' : frame_b64 })

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ImageForm()

    return render(request, 'index.html', {'xValues' : [] , 'yValues' : [], 'form': form})

def thanks(request):
    return HttpResponse('Thanks')
