import os, io
import cv2

def localize_objects(path,img):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'utils/capstone1057-a58de951c739.json'
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    height, width = img.shape[:2]

    objects = client.object_localization(
        image=image).localized_object_annotations

    CROPPER = []

    if len(objects)>1:
        print('Multiple Objects identified: {}'.format(len(objects)))
    else:
        for object_ in objects:
            if object_.name=='Book':
                print('\n{} (confidence: {})'.format(object_.name, object_.score))
                #print('Normalized bounding polygon vertices: ')
                for vertex in object_.bounding_poly.normalized_vertices:
                    vertex.x = vertex.x * width
                    vertex.y = vertex.y * height

                    # Add Vertex to cropped list
                    temp = (vertex.x, vertex.y)
                    CROPPER.append(temp)

                    #print(' - ({}, {})'.format(vertex.x * width, vertex.y * height))
            else:
                print('Paper Not Identified')

    # Get vertices from cropped list
    if len(CROPPER)>0:
        X1,Y1 = int(CROPPER[0][0]), int(CROPPER[0][1])
        X2,Y2 = int(CROPPER[2][0]), int(CROPPER[2][1])
        crop = img[Y1:Y2, X1:X2]
        cv2.imshow('Image', crop)
        cv2.waitKey(0)
        return crop
    else:
        cv2.imshow('Image', img)
        cv2.waitKey(0)
        return img

if __name__ == '__main__':

    path = 'PHOTOS/example3.jpg'
    img = cv2.imread(path)

    localize_objects(path, img)
