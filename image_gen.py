from PIL import Image, ImageFont, ImageDraw

X1_PATH = "props/x1.png"
X2_PATH = "props/x2.png"

GRAD1_PATH = "props/grad1.png"

TOP_TEXT = "Friendship ended with {old_friend_name}"
NOW_TEXT = "Now"
NEW_FRIEND_TEXT = "{new_friend_name}"
IS_MY_TEXT = "is my"
BEST_FRIEND_TEXT = "best friend"

def image_gen(back_path, left_path, right_path, old_friend_name, new_friend_name):

    back = Image.open(back_path)
    left = Image.open(left_path).convert("RGB")
    right = Image.open(right_path).convert("RGB")

    x1 = Image.open(X1_PATH)
    x2 = Image.open(X2_PATH)

    top_x_size = 800

    back_resized = back.resize((800, 600), resample=Image.Resampling.LANCZOS)
    left_resized = left.resize((172, 259), Image.Resampling.LANCZOS)
    right_resized = right.resize((221, 242), Image.Resampling.LANCZOS)

    left_resized.paste(x1, (0,0), x1)
    right_resized.paste(x2, (0,0), x2)

    back_resized.paste(left_resized, (0, 341))
    back_resized.paste(right_resized, (579, 358))
    
    pseudo_image_other = Image.new("RGBA", (800, 600), (255, 0, 0, 0))

    font_top = ImageFont.truetype("Arial Bold.ttf", size=50)

    grad_top = Image.open(GRAD1_PATH)
    alpha_top = Image.new("L", (1600, 600))

    draw_top = ImageDraw.Draw(alpha_top)

    draw_top.text((0, 40), TOP_TEXT.format(old_friend_name=old_friend_name), font=font_top, fill='white')

    grad_top.putalpha(alpha_top)
    #grad_top = grad_top.resize((800, 600))

    pseudo_image_top_resized = grad_top.resize((round(1600*0.8), round(600*2)))
    #pseudo_image_top_resized = grad_top

    other_text_layer = ImageDraw.Draw(pseudo_image_other)

    font_other = ImageFont.truetype("Arial Bold.ttf", size=38)

    other_text_layer.text((300, 70), NOW_TEXT, font=font_other, fill="#DF0676")
    other_text_layer.text((300, 110), NEW_FRIEND_TEXT.format(new_friend_name=new_friend_name).upper(), font=font_other, fill="#AB5955")
    other_text_layer.text((300, 150), IS_MY_TEXT, font=font_other, fill="#7C9535")
    other_text_layer.text((300, 185), BEST_FRIEND_TEXT, font=font_other, fill="#4CBF1F")

    pseudo_image_other_resized = pseudo_image_other.resize((800, round(600*2)))

    back_resized.paste(pseudo_image_top_resized, (0, -100), pseudo_image_top_resized)
    back_resized.paste(pseudo_image_other_resized, (0, -70), pseudo_image_other_resized)

    back.close()
    left.close()
    right.close()
    x1.close()
    x2.close()

    return back_resized