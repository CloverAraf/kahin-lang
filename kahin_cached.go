package main

/*
#cgo CFLAGS: -I/data/data/com.termux/files/usr/include/python3.11
#cgo LDFLAGS: -L/data/data/com.termux/files/usr/lib -lpython3.11
#include <Python.h>
#include <stdlib.h>
*/
import "C"
import (
	"archive/tar"
	"compress/gzip"
	"embed"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"unsafe"
)

//go:embed kahin_core.tar.gz
var CoreBundle embed.FS

var cachedLibPath string

const EngineCode = `import sys, tokenize, io, traceback, os

KEYWORDS = {
    "ice_aktar":"import","tanimla":"def","eger":"if","degilse_eger":"elif",
    "degilse":"else","dondu_boyunca":"while","her_biri_icin":"for","icinde":"in",
    "dondur":"return","yazdir":"print","girdi":"input","dur":"break",
    "devam_et":"continue","sinif":"class","dene":"try","yakala":"except",
    "sonunda":"finally","firlat":"raise","sil":"del","gec":"pass",
    "olumla":"assert","kuresel":"global","yerel_degil":"nonlocal",
    "lambda":"lambda","ile":"with","yukle":"yield","as":"as",
    "dogru":"True","yanlis":"False","hic":"None",
    "uzunluk":"len","aralik":"range","tam_sayi":"int","metin":"str",
    "ondalik":"float","liste":"list","sozluk":"dict","kume":"set",
    "demet":"tuple","tur":"type","yardim":"help","mutlak":"abs",
    "sirala":"sorted","ac":"open","topla":"sum","en_buyuk":"max",
    "en_kucuk":"min","bekle":"input",
    "sistem":"os","zaman":"time","istek":"requests","arayuz":"sys",
}

def transpile(source):
    lines = source.splitlines()
    result = []
    for line in lines:
        if line.strip().startswith("//"):
            result.append("#" + line.strip()[2:])
        else:
            result.append(line)
    source = "\n".join(result)

    tokens = []
    try:
        for tok in tokenize.tokenize(io.BytesIO(source.encode('utf-8')).readline):
            if tok.type == tokenize.NAME and tok.string in KEYWORDS:
                tokens.append((tok.type, KEYWORDS[tok.string]))
            else:
                tokens.append((tok.type, tok.string))
        return tokenize.untokenize(tokens).decode('utf-8')
    except:
        return source

def execute_kahin(file_path):
    if not os.path.exists(file_path):
        print(f"Hata: {file_path} bulunamadi")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    python_code = transpile(source)

    try:
        exec(python_code, {'__name__': '__main__'})
    except Exception as e:
        print(f"\nHata: {e}")
        traceback.print_exc()

if len(sys.argv) > 1:
    execute_kahin(sys.argv[1])
`

func setupLibOnce() string {
	// Cache kontrol - persistent dizin kullan
	cacheDir := os.Getenv("HOME") + "/.kahin_runtime"

	// Cache varsa hemen dön (hızlı!)
	if _, err := os.Stat(filepath.Join(cacheDir, "lib/python3.11")); err == nil {
		return cacheDir
	}

	// Cache yok, oluştur
	os.MkdirAll(cacheDir, 0755)

	f, _ := CoreBundle.Open("kahin_core.tar.gz")
	gz, _ := gzip.NewReader(f)
	tr := tar.NewReader(gz)

	for {
		header, err := tr.Next()
		if err == io.EOF {
			break
		}
		target := filepath.Join(cacheDir, header.Name)
		if header.Typeflag == tar.TypeDir {
			os.MkdirAll(target, 0755)
		} else {
			os.MkdirAll(filepath.Dir(target), 0755)
			outFile, _ := os.Create(target)
			io.Copy(outFile, tr)
			outFile.Close()
		}
	}

	return cacheDir
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Kahin v14.2 [Cached Runtime]")
		fmt.Println("Kullanim: ./kahin_cached <dosya.kahin>")
		return
	}

	// Setup lib (cache kullanır, ikinci çalıştırmada hızlı!)
	libPath := setupLibOnce()

	filePath := os.Args[1]
	os.Setenv("PYTHONPATH", libPath)
	os.Setenv("PYTHONHOME", libPath)

	launcher := fmt.Sprintf("import sys\nsys.path.insert(0, '%s')\nsys.argv = ['kahin', '%s']\n%s",
		libPath, filePath, strings.TrimSpace(EngineCode))

	cLauncher := C.CString(launcher)
	defer C.free(unsafe.Pointer(cLauncher))

	C.Py_Initialize()
	C.PyRun_SimpleString(cLauncher)
	C.Py_Finalize()
}
