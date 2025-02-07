import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='*', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

from keras.models import load_model # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

def get_class(model_path, labels_path, image_path):
    np.set_printoptions(suppress=True)
    model = load_model(model_path, compile=False)
    class_names = open(labels_path, "r").readlines()
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)
    
    return class_name

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{attachment.filename}")
            cikti = get_class("keras_model.h5", "labels.txt", f"./{attachment.filename}")
            if("Kedi" in cikti):
                cevap = "Kediler anatomik olarak güçlü, esnek bedenleriyle, hızlı refleksleriyle, keskin, geri çekilebilen pençeleriyle ve küçük avları öldürmeye uyarlanmış dişleriyle diğer kedigillere benzerler. Kediler, insan kulakları için çok zayıf ya da çok yüksek frekanstaki sesleri duyabilirler. Karanlığa yakın ortamlarda görebilirler. Çoğu memeli gibi, kediler insanlara göre daha zayıf renkli görüşe ve daha güçlü koku alma duyusuna sahiptir."
            elif("Köpek" in cikti):
                cevap = "Köpekler 12 binyıldan daha uzun bir süreden beri insanoğlunun av partneri, koruyucusu ve arkadaşı olmuştur. Değişik ihtiyaçlara göre farklı köpek türlerinin evrimleşmesinde insanoğlunun önemli rolü olmuştur. İlk köpekler keskin görme ve koku duyusuna sahip avcı köpekleridir. İnsanlar, ilk tanışmalarından bu yana köpeklerin çeşitli yararlı özelliklerini genetik mühendisliğin en ilkel formlarıyla ön plana çıkartmış ve farklı köpek türlerinin ortaya çıkmasını sağlamıştır. Örneğin 7-9 bin yıl önce çiftlik hayvanları evcilleştirildiğinde köpekler çobanlık da yapmaya başlamış ve bu yönde yapay seçilime uğramıştır."
            else:
                cevap = "Henüz fotoğraftaki şey eklenmedi :("
    else:
        await ctx.send("You forgot to upload the image :(")

    await ctx.send(cevap)

bot.run("TOKEN")
