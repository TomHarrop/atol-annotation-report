<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class UploadController extends Controller
{
    public function store(Request $request)
    {
        // simple validation
        $request->validate([
            'file_one' => 'required|file', // GFF
            'file_two' => 'required|file', // metadata csv
            'busco_results' => 'nullable|file',
            'omark_results' => 'nullable|file',
            'species_name' => 'nullable|string',
        ]);

        // Ensure uploads dir
        $uploadDir = storage_path('app/uploads');
        if (!is_dir($uploadDir)) {
            @mkdir($uploadDir, 0777, true);
        }

        // store files
        $gff = $request->file('file_one')->store('uploads');
        $meta = $request->file('file_two')->store('uploads');
        $busco = $request->hasFile('busco_results') ? $request->file('busco_results')->store('uploads') : null;
        $omark = $request->hasFile('omark_results') ? $request->file('omark_results')->store('uploads') : null;

    // prepare paths for script
    $script = storage_path('app/uploads/pipeline.py');
    $gffPath = storage_path('app/'.$gff);
    $buscoScript = storage_path('app/uploads/plot_BUSCO.py');
    $omarkScript = storage_path('app/uploads/plot_OMArk.py');
    $outputPdf = storage_path('app/uploads/results/output.pdf');

        // ensure public results dir
        $publicResults = public_path('results');
        if (!is_dir($publicResults)) {
            @mkdir($publicResults, 0777, true);
        }

        // Ensure results dir
        $outdir = storage_path('app/uploads/results');
        if (!is_dir($outdir)) { @mkdir($outdir, 0777, true); }

        // Build process for Python pipeline
        $cmd = [
            'python', $script,
            $gffPath,
            $buscoScript,
            $omarkScript,
            $outputPdf
        ];

        $process = new Process($cmd);
        $process->setTimeout(120);

        try {
            $process->run();
            if (! $process->isSuccessful()) {
                throw new ProcessFailedException($process);
            }

            $stdout = trim($process->getOutput());
            // pipeline.pl prints a JSON object on stdout in the mock
            $json = @json_decode($stdout, true);
            if (is_array($json) && !empty($json['status']) && $json['status'] === 'success' && !empty($json['output'])) {
                $resultPath = $json['output'];
                // copy result to public/results so it can be downloaded
                $basename = basename($resultPath);
                $publicFile = $publicResults.DIRECTORY_SEPARATOR.$basename;
                @copy($resultPath, $publicFile);

                $downloadUrl = url('results/'.$basename);
                return response()->json(['status'=>'success','output_url'=>$downloadUrl]);
            }

            // fallback: return whole stdout
            return response()->json(['status'=>'error','message'=>'Pipeline did not return success','raw'=>$stdout], 500);

        } catch (\Exception $e) {
            return response()->json(['status'=>'error','message'=>$e->getMessage()], 500);
        }
    }

    public function downloadResult($filename)
    {
        $path = public_path('results/'.$filename);
        if (!file_exists($path)) {
            abort(404);
        }
        return response()->download($path);
    }
}
