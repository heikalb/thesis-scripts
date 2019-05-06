import java.util.List;
import zemberek.morphology.TurkishMorphology;
import zemberek.morphology.analysis.SentenceAnalysis;
import zemberek.morphology.analysis.WordAnalysis;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.io.FileWriter;
import java.io.File;

public class ParseMorphemes
{
    public static void main (String[] args) throws IOException
    {
        // Corpus file
        File[] query_files = new File("../d2_data/joined/").listFiles();
        int i = 0;
        for(File f: query_files)
        {
            String dataFile = f.getName();
            FileReader fileReader = new FileReader("../d2_data/joined/" + dataFile);
            BufferedReader br = new BufferedReader(fileReader);

            // For Turkish morphological processing
            TurkishMorphology morphology = TurkishMorphology.createWithDefaults();

            //Collect parses
            ArrayList<List> parses = new ArrayList();

            // Go through lines in file
            String line;
            while ((line = br.readLine()) != null)
            {
                String sentence = line.split("\t")[0];
                List<WordAnalysis> analyses = morphology.analyzeSentence(sentence);
                SentenceAnalysis result = morphology.disambiguate(sentence, analyses);
                parses.add(result.bestAnalysis());
            }

            // Save data
            String path = "parses/" + dataFile.split("_")[0] +"_" + dataFile.split("_")[1] + "_parses.txt";
            File saveFile = new File(path);
            FileWriter writer = new FileWriter(saveFile);
            System.out.println(i + ": " + path);

            for(List parseList: parses)
                writer.append(parseList.toString() + '\n');

            writer.flush();
            writer.close();
            i++;
        }
    }
}
