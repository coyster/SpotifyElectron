import useFetch from 'hooks/useFetch';
import { useEffect } from 'react';
import ContextMenuSong from 'componentes/ContextMenu/Song/ContextMenuSong';
import styles from './explorar.module.css';

interface PropsExplorar {
  changeSongName: (songName: string) => void;
}

export default function Explorar(props: PropsExplorar) {
  // const {data} = useFetch("http://127.0.0.1:8000/canciones/p3")

  // const { data, loading, error } = useFetch("http://127.0.0.1:8000/listas/");

  /*   useEffect(() => {

    console.log(props.changeSongName)
  }, []) */

  return (
    <div className="container-fluid d-flex flex-column">
      <br />
      <br />
      <br />
      {/*       <ContextMenuSong />
       */}{' '}
    </div>
  );
}
