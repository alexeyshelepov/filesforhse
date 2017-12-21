package com.company;

import com.aliasi.chunk.Chunk;
import com.aliasi.chunk.Chunker;
import com.aliasi.chunk.Chunking;
import com.aliasi.dict.DictionaryEntry;
import com.aliasi.dict.ExactDictionaryChunker;
import com.aliasi.dict.MapDictionary;
import com.aliasi.tokenizer.IndoEuropeanTokenizerFactory;
import com.aliasi.util.AbstractExternalizable;


import opennlp.tools.namefind.*;
import opennlp.tools.util.*;
import opennlp.tools.util.eval.FMeasure;


import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.Set;


public class Main {

    public static void main(String[] args) {
        nerUsingTraining();
        //getEntitiesUsingChuncker();
    }


    private static final String sentences[] = {"Joe was the last person to see Fred. ",
            "He saw him in Boston at McKenzie's pub at 3:00 where he paid "
                    + "$2.45 for an ale. ",
            "Joe wanted to go to Vermont for the day to visit a cousin who "
                    + "works at IBM, but Sally and he had to look for Fred"};

    private static void getEntitiesUsingChuncker() {
        useMlChunker();
        //useSimpleDictionary();
    }

    private static void useMlChunker() {
        try {
            File modelFile = new File(
                    "C:\\machine_learning\\src\\com\\company\\ne-en-news-muc6.AbstractCharLmRescoringChunker");
            Chunker chunker
                    = (Chunker) AbstractExternalizable.readObject(modelFile);

            for (String sentence : sentences) {
                displayChunkSet(chunker, sentence);
            }
        } catch (IOException | ClassNotFoundException ex) {
            ex.printStackTrace();
        }
    }

    private static void displayChunkSet(Chunker chunker, String text) {
        Chunking chunking = chunker.chunk(text);
        Set<Chunk> set = chunking.chunkSet();
        for (Chunk chunk : set) {
            System.out.println("Type: " + chunk.type() + " Entity: ["
                    + text.substring(chunk.start(), chunk.end())
                    + "] Score: " + chunk.score());
        }
    }

    private static MapDictionary<String> initializeDictionary() {
        MapDictionary<String> dictionary = new MapDictionary<>();
        dictionary.addEntry(
                new DictionaryEntry<>("Joe", "PERSON", 1.0));
        dictionary.addEntry(
                new DictionaryEntry<>("Fred", "PERSON", 1.0));
        dictionary.addEntry(
                new DictionaryEntry<>("Boston", "PLACE", 1.0));
        dictionary.addEntry(
                new DictionaryEntry<>("pub", "PLACE", 1.0));
        dictionary.addEntry(
                new DictionaryEntry<>("Vermont", "PLACE", 1.0));
        dictionary.addEntry(
                new DictionaryEntry<>("IBM", "ORGANIZATION", 1.0));
        dictionary.addEntry(
                new DictionaryEntry<>("Sally", "PERSON", 1.0));

        return  dictionary;
    }

    private static void useSimpleDictionary() {
        MapDictionary<String> dictionary =  initializeDictionary();
        System.out.println("\nDICTIONARY\n" + dictionary);

        ExactDictionaryChunker dictionaryChunker
                = new ExactDictionaryChunker(dictionary,
                IndoEuropeanTokenizerFactory.INSTANCE, true, false);

        for (String sentence : sentences) {
            System.out.println("\nTEXT=" + sentence);
            displayChunkSet(dictionaryChunker, sentence);
        }
    }


    private static void nerUsingTraining() {
        try (OutputStream modelOutputStream = new BufferedOutputStream(
                new FileOutputStream(new File("modelFile")))) {
            //ObjectStream<String> lineStream = new PlainTextByLineStream(
            //        new FileInputStream("en-ner-person.train"), "UTF-8");
            InputStreamFactory factory = () -> new FileInputStream("C:\\machine_learning\\src\\com\\company\\en-ner-person.train");
            ObjectStream<String> lineStream = new PlainTextByLineStream(
                    factory, "UTF-8"
            );
            ObjectStream<NameSample> sampleStream = new NameSampleDataStream(lineStream);

            TokenNameFinderFactory finderFactory = new TokenNameFinderFactory();

            TrainingParameters parameters = new TrainingParameters();
            parameters.put(TrainingParameters.CUTOFF_PARAM, "5");
            parameters.put(TrainingParameters.ITERATIONS_PARAM, "100");


            TokenNameFinderModel model = NameFinderME.train("en", "person", sampleStream,
                    parameters, finderFactory);

            model.serialize(modelOutputStream);

            System.out.println("TokenNameFinderEvaluator");
            TokenNameFinderEvaluator evaluator = new TokenNameFinderEvaluator(new NameFinderME(model));

            InputStreamFactory evalFactory = () -> new FileInputStream("C:\\machine_learning\\src\\com\\company\\en-ner-person.eval");

            lineStream = new PlainTextByLineStream(
                    evalFactory, "UTF-8");
            sampleStream = new NameSampleDataStream(lineStream);
            evaluator.evaluate(sampleStream);

            FMeasure result = evaluator.getFMeasure();
            System.out.println(result.toString());
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
}
