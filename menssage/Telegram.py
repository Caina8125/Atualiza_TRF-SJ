import requests


def Dev(aviso):
    proxies = {
        "http": f"http://lucas.timoteo:Caina8125@10.0.0.230:3128/",
        "https": f"http://lucas.timoteo:Caina8125@10.0.0.230:3128/"
    }

    my_id   = '1148462305'
    myToken = '6958350096:AAHxsXXkiOjPrLMe0NRllYUGmkdDSzRJjh8'
    teste = requests.post(f'https://api.telegram.org/bot{myToken}/sendMessage?chat_id={my_id}&text='+aviso, proxies=proxies)
    print(teste)


def Amhp(aviso):
    proxies = {
        "http": f"http://lucas.timoteo:Caina8125@10.0.0.230:3128/",
        "https": f"http://lucas.timoteo:Caina8125@10.0.0.230:3128/"
    }

    amhp_id   = '-357797147'
    myToken = '6958350096:AAHxsXXkiOjPrLMe0NRllYUGmkdDSzRJjh8'
    requests.post(f'https://api.telegram.org/bot{myToken}/sendMessage?chat_id={amhp_id}&text='+aviso, proxies=proxies)



# Dev("*Relatório TRF/SJ*\n \n 2019 Beneficiários do SJ atualizados no AMHPTISS;\n \n 19542 Beneficiários do SJ atualizados no AMHPTISS;")