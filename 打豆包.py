import pygame
import random

pygame.init()
pygame.mixer.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("打豆包")
clock = pygame.time.Clock()

# 颜色
BG_COLOR = (240, 248, 255)
BLUE = (50, 120, 255)
RED_BAO = (220, 40, 40)
GOLD = (255, 210, 0)
GRENADE = (80, 80, 80)
HIT_RED = (255, 80, 80)
BLACK = (0,0,0)
WHITE = (255,255,255)
BTN_COLOR = (70, 150, 240)
BTN_HOVER = (110, 185, 255)

# 背景音乐 Aria Math
try:
    pygame.mixer.music.load("Aria Math.wav")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
except:
    pass

score = 0
font = pygame.font.SysFont("simhei", 48)
tip_font = pygame.font.SysFont("simhei", 60)
end_font = pygame.font.SysFont("simhei", 80)
btn_font = pygame.font.SysFont("simhei", 32)
title_font = pygame.font.SysFont("simhei", 72)
taunt_font = pygame.font.SysFont("simhei", 90)

bao_r = 60
region_size = 180
cx, cy = W // 2, H // 2
region_left = cx - region_size
region_top = cy - region_size
region_right = cx + region_size
region_bot = cy + region_size

bao_x = 0
bao_y = 0
bao_type = "blue"
hit_red_timer = 0
hit_red_duration = 0.6
state = "menu"  # menu 选难度 / play 游戏 / over 结束 / taunt 嘲讽弹窗
difficulty = None
death_count = 0

# 30秒定时弹窗相关
taunt_timer = 0.0
taunt_trigger_enable = False

# 难度配置
diff_cfg = {
    "easy": {
        "blue":0.60,
        "red":0.25,
        "gold":0.10,
        "grenade":0.05
    },
    "normal": {
        "blue":0.675,
        "red":0.125,
        "gold":0.05,
        "grenade":0.15
    },
    "hard": {
        "blue":0.6625,
        "red":0.0625,
        "gold":0.025,
        "grenade":0.25
    }
}

# 难度按钮
btn_easy = pygame.Rect(0, 0, 260, 75)
btn_easy.center = (W//2, H//2 - 100)
btn_normal = pygame.Rect(0, 0, 260, 75)
btn_normal.center = (W//2, H//2)
btn_hard = pygame.Rect(0, 0, 260, 75)
btn_hard.center = (W//2, H//2 + 100)

restart_btn = pygame.Rect(0, 0, 220, 70)
restart_btn.center = (W//2, H//2 + 120)

taunt_btn = pygame.Rect(0,0,240,80)
taunt_btn.center = (W//2, H//2 + 100)

# 右上角重置豆包按钮
reset_bao_btn = pygame.Rect(W - 140, 10, 130, 45)

float_texts = []

def reset_bao():
    global bao_x, bao_y, bao_type
    cfg = diff_cfg[difficulty]
    bao_x = random.randint(region_left + bao_r, region_right - bao_r)
    bao_y = random.randint(region_top + bao_r, region_bot - bao_r)
    r = random.random()
    if r < cfg["blue"]:
        bao_type = "blue"
    elif r < cfg["blue"] + cfg["red"]:
        bao_type = "red"
    elif r < cfg["blue"] + cfg["red"] + cfg["gold"]:
        bao_type = "gold"
    else:
        bao_type = "grenade"

def reset_game():
    global score, float_texts
    score = 0
    float_texts.clear()
    reset_bao()

running = True
while running:
    dt = clock.tick(60) / 1000.0
    mouse_pos = pygame.mouse.get_pos()

    if hit_red_timer > 0:
        hit_red_timer -= dt

    if taunt_trigger_enable and state == "play":
        taunt_timer += dt
        if taunt_timer >= 30.0:
            state = "taunt"
            taunt_timer = 0.0

    # 飘字更新
    new_float = []
    for txt, x, y, alpha in float_texts:
        y -= 120 * dt
        alpha -= 180 * dt
        if alpha > 0:
            new_float.append((txt, x, y, alpha))
    float_texts = new_float

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if state == "menu":
                if btn_easy.collidepoint(mx, my):
                    difficulty = "easy"
                    reset_game()
                    state = "play"
                    taunt_trigger_enable = False
                    taunt_timer = 0
                elif btn_normal.collidepoint(mx, my):
                    difficulty = "normal"
                    reset_game()
                    state = "play"
                    taunt_trigger_enable = False
                    taunt_timer = 0
                elif btn_hard.collidepoint(mx, my):
                    difficulty = "hard"
                    reset_game()
                    state = "play"
                    taunt_trigger_enable = False
                    taunt_timer = 0

            elif state == "over":
                if restart_btn.collidepoint(mx, my):
                    reset_game()
                    state = "play"

            elif state == "taunt":
                if taunt_btn.collidepoint(mx, my):
                    reset_game()
                    state = "play"
                    taunt_trigger_enable = True
                    taunt_timer = 0.0

            elif state == "play":
                # 右上角重置豆包按钮
                if reset_bao_btn.collidepoint(mx, my):
                    reset_bao()
                else:
                    dx = mx - bao_x
                    dy = my - bao_y
                    if dx*dx + dy*dy <= bao_r*bao_r:
                        hit_red_timer = hit_red_duration
                        if bao_type == "blue":
                            add = 1
                            score += add
                            float_texts.append((f"+{add}", bao_x, bao_y, 255))
                            reset_bao()
                        elif bao_type == "red":
                            add = 2
                            score += add
                            float_texts.append((f"+{add}", bao_x, bao_y, 255))
                            reset_bao()
                        elif bao_type == "gold":
                            add = 5
                            score += add
                            float_texts.append((f"+{add}", bao_x, bao_y, 255))
                            reset_bao()
                        elif bao_type == "grenade":
                            death_count += 1
                            if death_count >= 10:
                                state = "taunt"
                            else:
                                state = "over"

    screen.fill(BG_COLOR)

    if state == "menu":
        title_surf = title_font.render("选择难度", True, BLACK)
        title_rect = title_surf.get_rect(center=(W//2, H//2 - 200))
        screen.blit(title_surf, title_rect)

        c = BTN_HOVER if btn_easy.collidepoint(mouse_pos) else BTN_COLOR
        pygame.draw.rect(screen, c, btn_easy, border_radius=12)
        t = btn_font.render("简单", True, WHITE)
        screen.blit(t, t.get_rect(center=btn_easy.center))

        c = BTN_HOVER if btn_normal.collidepoint(mouse_pos) else BTN_COLOR
        pygame.draw.rect(screen, c, btn_normal, border_radius=12)
        t = btn_font.render("普通", True, WHITE)
        screen.blit(t, t.get_rect(center=btn_normal.center))

        c = BTN_HOVER if btn_hard.collidepoint(mouse_pos) else BTN_COLOR
        pygame.draw.rect(screen, c, btn_hard, border_radius=12)
        t = btn_font.render("困难", True, WHITE)
        screen.blit(t, t.get_rect(center=btn_hard.center))

    elif state == "play":
        pygame.draw.rect(screen, BLACK, (region_left, region_top, region_size*2, region_size*2), 3)
        if hit_red_timer > 0:
            c = HIT_RED
        else:
            if bao_type == "blue":
                c = BLUE
            elif bao_type == "red":
                c = RED_BAO
            elif bao_type == "gold":
                c = GOLD
            else:
                c = GRENADE
        pygame.draw.circle(screen, c, (bao_x, bao_y), bao_r)

        s_surf = font.render(f"分数：{score}", True, BLACK)
        screen.blit(s_surf, (20, 20))

        # 右上角重置豆包按钮绘制
        btn_color = BTN_HOVER if reset_bao_btn.collidepoint(mouse_pos) else BTN_COLOR
        pygame.draw.rect(screen, btn_color, reset_bao_btn, border_radius=8)
        text = btn_font.render("重置豆包", True, WHITE)
        text_rect = text.get_rect(center=reset_bao_btn.center)
        screen.blit(text, text_rect)

        for txt, x, y, alpha in float_texts:
            if txt == "+1":
                color = BLUE
            elif txt == "+2":
                color = RED_BAO
            elif txt == "+5":
                color = GOLD
            else:
                color = BLACK
            surf = tip_font.render(txt, True, color)
            surf.set_alpha(max(0, int(alpha)))
            rect = surf.get_rect(center=(x, y))
            screen.blit(surf, rect)

    elif state == "over":
        end_surf = end_font.render("游戏结束", True, RED_BAO)
        end_rect = end_surf.get_rect(center=(W//2, H//2 - 40))
        screen.blit(end_surf, end_rect)

        pygame.draw.rect(screen, BTN_COLOR, restart_btn, border_radius=12)
        btn_surf = btn_font.render("重新开始", True, WHITE)
        btn_surf_rect = btn_surf.get_rect(center=restart_btn.center)
        screen.blit(btn_surf, btn_surf_rect)

    elif state == "taunt":
        text_surf = taunt_font.render("菜就多练", True, RED_BAO)
        text_rect = text_surf.get_rect(center=(W//2, H//2 - 60))
        screen.blit(text_surf, text_rect)

        btn_color = BTN_HOVER if taunt_btn.collidepoint(mouse_pos) else BTN_COLOR
        pygame.draw.rect(screen, btn_color, taunt_btn, border_radius=12)
        btn_text = btn_font.render("滚出去", True, WHITE)
        btn_text_rect = btn_text.get_rect(center=taunt_btn.center)
        screen.blit(btn_text, btn_text_rect)

    pygame.display.flip()

pygame.quit()
