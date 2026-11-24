import sys
from logica import ejecutar_simulacion_completa, comparar_dos_escenarios

def test_caso_verificacion():
    perfil = [0.0, 0.5, 1.0, 0.5]
    consumo = [1.0, 1.0, 1.0, 1.0]
    paneles = 4
    kw_panel = 0.5
    perdidas = 0.20
    tarifa = 800

    print("=== TEST CASO DE VERIFICACIÓN (NORMAL) ===")
    res = ejecutar_simulacion_completa(perfil, consumo, paneles, kw_panel, perdidas, tarifa, factor_clima=1.0)
    
    gen = res["perfiles"]["generacion"]
    auto = res["indicadores"]["total_autoconsumo"]
    cob = res["indicadores"]["porcentaje_cubierto"]
    exc = res["indicadores"]["total_excedente"]
    ahorro = res["indicadores"]["ahorro_dia"]
    
    print(f"Generación horaria esperada [0.0, 0.8, 1.6, 0.8]: {gen}")
    assert gen == [0.0, 0.8, 1.6, 0.8], f"Error en generación: {gen}"

    print(f"Autoconsumo esperado 2.6 kWh: {auto}")
    assert auto == 2.6, f"Error en autoconsumo: {auto}"

    print(f"Cobertura esperada 65.0%: {cob}")
    assert cob == 65.0, f"Error en porcentaje cubierto: {cob}"

    print(f"Excedente esperado 0.6 kWh: {exc}")
    assert exc == 0.6, f"Error en excedente: {exc}"

    print(f"Ahorro esperado $2,080: {ahorro}")
    assert ahorro == 2080.0, f"Error en ahorro: {ahorro}"

    print("\n=== TEST DÍA NUBLADO (PERFIL X 0.5) ===")
    res_nublado = ejecutar_simulacion_completa(perfil, consumo, paneles, kw_panel, perdidas, tarifa, factor_clima=0.5)
    
    perfil_nub = res_nublado["perfiles"]["perfil_solar"]
    gen_nub = res_nublado["perfiles"]["generacion"]
    auto_nub = res_nublado["indicadores"]["total_autoconsumo"]
    exc_nub = res_nublado["indicadores"]["total_excedente"]

    print(f"Perfil nublado esperado [0.0, 0.25, 0.5, 0.25]: {perfil_nub}")
    assert perfil_nub == [0.0, 0.25, 0.5, 0.25], f"Error en perfil nublado: {perfil_nub}"

    print(f"Autoconsumo nublado esperado 1.6 kWh: {auto_nub}")
    assert auto_nub == 1.6, f"Error en autoconsumo nublado: {auto_nub}"

    print(f"Excedente nublado esperado 0.0 kWh: {exc_nub}")
    assert exc_nub == 0.0, f"Error en excedente nublado: {exc_nub}"

    print("\n=== TEST COMPARACIÓN 4 vs 8 PANELES ===")
    esc_4 = {"nombre": "4 Paneles", **res}
    res_8 = ejecutar_simulacion_completa(perfil, consumo, 8, kw_panel, perdidas, tarifa, factor_clima=1.0)
    esc_8 = {"nombre": "8 Paneles", **res_8}
    comp = comparar_dos_escenarios(esc_4, esc_8)
    print(f"Ganador: {comp['ganador']}")
    print(f"Diferencia Ahorro: {comp['diferencia_ahorro']}")
    print(f"Explicación: {comp['explicacion']}")

    print("\n>>> ¡TODOS LOS TESTS PASARON EXITOSAMENTE CON 100% DE PRECISIÓN! <<<")

if __name__ == "__main__":
    test_caso_verificacion()
