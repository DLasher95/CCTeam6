import torch
import matplotlib.pyplot as plt
import numpy as np
import argparse
import pickle
import os
from torchvision import transforms
from Auto_Image_Captioning.building_vocab import Vocabulary
from Auto_Image_Captioning.model import EncoderCNN, DecoderRNN
from PIL import Image
<<<<<<< Updated upstream
from extract_colors import DominantColors
from color_emotions import color_check
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
=======
from Auto_Image_Captioning.extract_colors import DominantColors

>>>>>>> Stashed changes
"""
Author: Dylan Lasher
Specs: Python 3.7, Windows 10
Purpose: A sample-run of a CNN-RNN auto-captioning tool.
"""
# ***Directions at the bottom ***

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_image(image_path, transform=None):
    image = Image.open(image_path)
    image = image.resize([224, 224], Image.LANCZOS)
    
    if transform is not None:
        image = transform(image).unsqueeze(0)
    
    return image

def main(args):
    # Image preprocessing
    transform = transforms.Compose([
        transforms.ToTensor(), 
        transforms.Normalize((0.485, 0.456, 0.406), 
                             (0.229, 0.224, 0.225))])
    
    # Load vocabulary wrapper
    with open(args.vocab_path, 'rb') as f:
        vocab = pickle.load(f)

    # Build models
    encoder = EncoderCNN(args.embed_size).eval()
    decoder = DecoderRNN(args.embed_size, args.hidden_size, len(vocab), args.num_layers)
    encoder = encoder.to(device)
    decoder = decoder.to(device)

    # Load trained model parameters
    encoder.load_state_dict(torch.load(args.encoder_path))
    decoder.load_state_dict(torch.load(args.decoder_path))

    # Prepare image
    image = load_image(args.image, transform)
    image_tensor = image.to(device)
    
    # Generate caption for image
    feature = encoder(image_tensor)
    sampled_ids = decoder.sample(feature)
    sampled_ids = sampled_ids[0].cpu().numpy()

    # Run color analysis
    clusters = int(args.colors)

    # Number of dominant colors you will find.
    dc = DominantColors(args.image, clusters)
    colors = dc.dominantColors()

    # Convert extracted colors to emotions
    # (colors = array of identified colors)
    closest_names = []
    for i in range(len(colors)):
        closest_color_weird_format = color_check.closest(color_check.color_list, colors[i])
        closest_color_use = [closest_color_weird_format[0][0], closest_color_weird_format[0][1],
                             closest_color_weird_format[0][2]]
        for keys in color_check.colors:
            if color_check.colors.get(keys) == closest_color_use:
                closest_names.append(keys)
    found_emotions = color_check.find_emotions(closest_names)

    # Convert word_ids to words
    sampled_caption = []
    for word_id in sampled_ids:
        word = vocab.idx2word[word_id]
        if word == '<end>':
            # Add mood description.
            sampled_caption.append( "This image has colors that indicate emotional tones of ")
            # ToDo: Append emotional words
            for i in range(len(found_emotions)):
                sampled_caption.append(found_emotions[i])
                sampled_caption.append(",")
            sampled_caption.append(word)
            break
        sampled_caption.append(word)
    sentence = ' '.join(sampled_caption)
    
    # Print image and generated caption
    print (sentence)
    # print(colors) # Uncomment to print RGB values of colors
    image = Image.open(args.image)
    plt.imshow(np.asarray(image))

    # Plot histogram
    dc.plotHistogram()
    plt.savefig("myHistogram.png")

    # Create array of important words
    sentence = sentence.replace("This image has colors that indicate emotional tones of", "")
    sentence = sentence.replace("<start>", "")
    sentence = sentence.replace("<end>", "")
    exclude = set(string.punctuation)
    sentence = ''.join(ch for ch in sentence if ch not in exclude) # Remove punctuation
    stop_words = set(stopwords.words('english'))
    word_tokens = nltk.word_tokenize(sentence)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    # Print results
    print (sentence)
    print(filtered_sentence)
"""
To run, go to Terminal and type:
  python sample.py --image picture_location --colors num_of_colors
  (where picture_location is the image. Example: images/ball.jpg)
  (num_of_colors is the number of dominant colors you want. Example: 4)
  
  Example: python sample.py --image images/ball.jpg --colors 4
  If Auto_Image_Captioningisin a nestedfolder, keep that in mind for the script call.
  
  To grab the array of important words, grab the filtered_sentence array from this class
  
  Check myHistogram.png for the histogram of extracted colors
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True, help='input image for generating caption')
    parser.add_argument('--colors', type=str, required=True, help='number of dominant colors')
    parser.add_argument('--encoder_path', type=str, default='models/encoder-5-3000.pkl', help='path for trained encoder')
    parser.add_argument('--decoder_path', type=str, default='models/decoder-5-3000.pkl', help='path for trained decoder')
    parser.add_argument('--vocab_path', type=str, default='data/vocab.pkl', help='path for vocabulary wrapper')
    
    # Model parameters (should be same as parameters in train.py)
    parser.add_argument('--embed_size', type=int , default=256, help='dimension of word embedding vectors')
    parser.add_argument('--hidden_size', type=int , default=512, help='dimension of lstm hidden states')
    parser.add_argument('--num_layers', type=int , default=1, help='number of layers in lstm')
    args = parser.parse_args()
    main(args)
